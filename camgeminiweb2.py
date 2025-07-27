import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
from picamera2 import Picamera2
import time
from collections import Counter
import requests
import json
from qrcode import scan_qr
from price_reader import get_price
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
from datetime import datetime
import serial
from bill_display import show_bill


arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Wait for connection



class FoodRecommendationGUI:
    p=0
    def __init__(self, root):
        self.current_item = None
        self.current_weight = 0
        self.current_price = 0
        self.cart_file = "cart.json"

        self.root = root
        self.root.title("HealthSync")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.disease = None
        self.is_running = False
        self.last_prediction = ""
        self.predictions = []
        self.current_status = "Initializing..."
        
        # Gemini API config
        self.API_KEY = "AIzaSyCSC30QskGtSn3NhRuuOQTMq1R6_KHkxWA"
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.API_KEY}"
        self.headers = {"Content-Type": "application/json"}
        
        # Create GUI elements
        self.create_widgets()
        
        # Initialize camera and model
        self.initialize_system()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="HealthSync", 
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=10)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Left side - Camera view
        camera_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        camera_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        camera_title = tk.Label(
            camera_frame, 
            text="Camera View", 
            font=('Arial', 14, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        camera_title.pack(pady=5)
        
        # Camera display
        self.camera_label = tk.Label(camera_frame, bg='#34495e')
        self.camera_label.pack(pady=10, padx=10)
        
        # Right side - Information panel
        info_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        info_frame.pack(side='right', fill='y', padx=(10, 0))
        info_frame.configure(width=300)
        
        
    
        # Disease info section
        disease_title = tk.Label(
            info_frame, 
            text="Health Condition", 
            font=('Arial', 14, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        disease_title.pack(pady=(20, 5))
        
        self.disease_label = tk.Label(
            info_frame,
            text="Scan QR code to set condition",
            font=('Arial', 12),
            bg='#34495e',
            fg='#e74c3c',
            wraplength=280,
            justify='center'
        )
        self.disease_label.pack(pady=5, padx=10)
        
        # Detection section
        detection_title = tk.Label(
            info_frame, 
            text="Food Detection", 
            font=('Arial', 14, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        detection_title.pack(pady=(20, 5))
        
        self.detection_label = tk.Label(
            info_frame,
            text="No food detected",
            font=('Arial', 12),
            bg='#34495e',
            fg='#95a5a6',
            wraplength=280,
            justify='center'
        )
        self.detection_label.pack(pady=5, padx=10)
        
        # Recommendation section
        recommendation_title = tk.Label(
            info_frame, 
            text="AI Recommendation", 
            font=('Arial', 20, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        recommendation_title.pack(pady=(20, 5))
        
        # Create scrollable text widget for recommendations
        rec_frame = tk.Frame(info_frame, bg='#34495e')
        rec_frame.pack(pady=5, padx=10, fill='both', expand=True)
        
        self.recommendation_text = tk.Text(
            rec_frame,
            height=10,
            width=50,
            font=('Arial', 15, 'normal'),
            bg='#1a252f',
            fg='#ffffff',
            wrap='word',
            relief='raised',
            bd=2,
            insertbackground='#3498db',
            selectbackground='#3498db',
            selectforeground='#ffffff'
        )
        self.recommendation_text.pack(side='left', fill='both', expand=True)
        
        # Scrollbar for recommendation text
        scrollbar = ttk.Scrollbar(rec_frame, orient='vertical', command=self.recommendation_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.recommendation_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure text tags for better formatting
       # self.recommendation_text.tag_configure("timestamp", foreground="#95a5a6", font=('Arial', 9, 'italic'))
        self.recommendation_text.tag_configure("food_item", foreground="#f39c12", font=('Arial', 11, 'bold'))
        self.recommendation_text.tag_configure("recommendation", foreground="#ecf0f1", font=('Arial', 10, 'normal'))
        self.recommendation_text.tag_configure("good", foreground="#2ecc71", font=('Arial', 20, 'bold'))
        self.recommendation_text.tag_configure("bad", foreground="#e74c3c", font=('Arial', 20, 'bold'))
        self.recommendation_text.tag_configure("separator", foreground="#34495e")
        
        # Control buttons
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(
            button_frame,
            text="🚀 Start Detection",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.start_detection,
            padx=20,
            pady=5
        )
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = tk.Button(
            button_frame,
            text="Add to Cart",
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            command=self.stop_detection,
            padx=20,
            pady=5,
            state='disabled'
        )
        self.stop_button.pack(side='left', padx=5)
        
        self.scan_qr_button = tk.Button(
            button_frame,
            text="Print Bill",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            command=self.scan_qr_code,
            padx=20,
            pady=5
        )
        self.scan_qr_button.pack(side='left', padx=5)
        
        # Initial message in recommendation area
        self.recommendation_text.insert(tk.END, "Welcome to Smart Food Recommendation System! n\n", "food_item")
        self.recommendation_text.insert(tk.END, "Quick Start Guide:\n", "food_item")
        self.recommendation_text.insert(tk.END, "1️⃣ First, scan a QR code with your health condition\n", "recommendation")
        self.recommendation_text.insert(tk.END, "2️⃣ Point camera at food items for AI recommendations\n\n", "recommendation")
       
        self.recommendation_text.insert(tk.END, "System is ready to help you make healthier food choices!\n", "good")
        self.recommendation_text.insert(tk.END, "="*42 + "\n\n", "separator")
        self.recommendation_text.configure(state='disabled')
        
    def initialize_system(self):
        try:
            self.update_status("Initializing camera...")
            
            # Initialize PiCamera
            self.picam2 = Picamera2()
            self.picam2.configure(self.picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
            self.picam2.set_controls({"AwbEnable": True, "AeEnable": True})
            self.picam2.start()
            time.sleep(2)
            
            self.update_status("Loading AI model...")
            
            # Load TFLite model
            model_path = "/home/robo/hackthon/converted_tflite/model_unquant.tflite"
            self.interpreter = tflite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            
            # Tensor info
            self.input_details = self.interpreter.get_input_details()
            self.input_index = self.input_details[0]['index']
            self.input_shape = self.input_details[0]['shape']
            self.output_details = self.interpreter.get_output_details()
            self.output_index = self.output_details[0]['index']
            
            # Load labels
            with open("/home/robo/hackthon/converted_tflite/labels.txt", 'r') as f:
                self.labels = [line.strip().split(' ', 1)[1] for line in f.readlines()]
            
            # Prediction smoothing
            self.prediction_window_seconds = 3
            self.fps_estimate = 10
            self.window_size = self.prediction_window_seconds * self.fps_estimate
            
            self.update_status("System initialized successfully! Ready to scan QR code.")
            
            # Start camera display after successful initialization
            self.update_camera_display()
            
        except Exception as e:
            self.update_status(f"Error initializing system: {str(e)}")
            # Show placeholder in camera area if initialization fails
            self.camera_label.configure(text="Camera not available", fg='red')
    
    def update_status(self, message):
        self.current_status = message
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
# Replace your scan_qr_code method with this updated version:

    def scan_qr_code(self):
        # If disease is already set, show bill instead of scanning QR
        if self.disease:
            try:
                show_bill()  # This opens the bill window
                self.update_status("Bill window opened")
            except Exception as e:
                self.update_status(f"Error opening bill: {str(e)}")
            return
        
        # First time - scan QR code
        self.disease_label.configure(text=f"Scan QR Code")
        self.update_status("Scanning QR code... Please show QR code to camera")
        if self.is_running:
            self.stop_detection()
        try:
            # Use threading to prevent GUI freeze during QR scanning
            def qr_scan_thread():
                try:
                    disease = scan_qr(self.picam2)
                    # Update GUI from main thread
                    self.root.after(0, lambda: self.handle_qr_result(disease))
                except Exception as e:
                    self.root.after(0, lambda: self.update_status(f"QR scan error: {str(e)}"))
            
            thread = threading.Thread(target=qr_scan_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.update_status(f"QR scan error: {str(e)}")
    def handle_qr_result(self, disease):
        if disease:
            self.disease = disease
            self.disease_label.configure(text=f"Condition: {self.disease}", fg='#2ecc71')
            self.update_status("QR code scanned successfully!")

            self.add_formatted_recommendation(
                "✅ HEALTH CONDITION SET",
                f"Condition: {self.disease}\nReady to analyze food items!",
                "good"
            )

            # Start detection automatically after QR is scanned
            self.start_detection()

        else:
            self.disease_label.configure(text="No QR code detected", fg='#e74c3c')

    def start_detection(self):
        
        if not self.disease:
            self.update_status("Please scan QR code first!")
            return
        
        self.is_running = True
        self.start_button.configure(state='disabled')
        self.stop_button.configure(state='normal')
        self.predictions = []
        self.last_prediction = ""
        
        self.update_status("Food detection started...")
        
        # Start detection in separate thread
        self.detection_thread = threading.Thread(target=self.detection_loop)
        self.detection_thread.daemon = True
        self.detection_thread.start()
        
    def save_to_cart(self, item_name, weight, price):
        """Save item to cart JSON file"""
        try:
            # Try to load existing cart
            try:
                with open(self.cart_file, 'r') as f:
                    cart = json.load(f)
            except FileNotFoundError:
                cart = {"items": [], "total": 0}
            
            # Add new item
            new_item = {
                "name": item_name,
                "weight_grams": int(weight),
                "price_per_kg": get_price(item_name),
                "total_price": round(price, 2),
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            cart["items"].append(new_item)
            cart["total"] = round(sum(item["total_price"] for item in cart["items"]), 2)
            
            # Save updated cart
            with open(self.cart_file, 'w') as f:
                json.dump(cart, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error saving to cart: {e}")
            return False

# Update your stop_detection method (replace the existing one):
    def stop_detection(self):
        """Add current item to cart"""
        if self.current_item and self.current_weight > 0:
            success = self.save_to_cart(self.current_item, self.current_weight, self.current_price)
            if success:
                self.add_formatted_recommendation(
                    f"🛒 ADDED TO CART",
                    f"Item: {self.current_item}\nWeight: {self.current_weight}g\nPrice: ${self.current_price:.2f}",
                    "good"
                )
                self.update_status(f"Added {self.current_item} to cart!")
            else:
                self.update_status("Error adding item to cart!")
        else:
            self.update_status("No item detected to add to cart!")


    
    def detection_loop(self):
        while self.is_running:
            try:
                # Capture image safely
                if not hasattr(self, 'picam2'):
                    self.update_status("Camera not available for detection")
                    break
                    
                image = self.picam2.capture_array()
                
                # Prepare image for model with proper error handling
                try:
                    img = cv2.resize(image, (self.input_shape[1], self.input_shape[2]))
                    img = img.astype(np.float32) / 255.0  # Normalize first, then convert
                    img = np.expand_dims(img, axis=0)
                    
                    # Ensure tensor shape is correct
                    if img.shape != tuple(self.input_shape):
                        self.update_status(f"Tensor shape mismatch: expected {self.input_shape}, got {img.shape}")
                        continue
                    
                    # Run inference with error handling
                    self.interpreter.set_tensor(self.input_index, img)
                    self.interpreter.invoke()
                    output_data = self.interpreter.get_tensor(self.output_index)
                    
                    # Ensure output data is valid
                    if output_data is None or len(output_data) == 0:
                        continue
                        
                    top_prediction = np.argmax(output_data)
                    
                    # Validate prediction index
                    if top_prediction >= len(self.labels):
                        continue
                        
                    predicted_label = self.labels[top_prediction]
                    
                    # Smoothing
                    self.predictions.append(predicted_label)
                    if len(self.predictions) > self.window_size:
                        self.predictions.pop(0)
                    
                    if len(self.predictions) > 0:
                        common_prediction = Counter(self.predictions).most_common(1)[0][0]
                        
                        # Update detection display
                        if common_prediction != "nothing":
                            price = get_price(common_prediction)
                            

                            if arduino.in_waiting > 0:
                                total_w = arduino.readline().decode('utf-8').strip()
                                if total_w:
                                    print(f"Received: {total_w}")
                                    w_price = price * int(total_w) / 1000
                                    
                                    # Store current item data for cart
                                    self.current_item = common_prediction
                                    self.current_weight = int(total_w)
                                    self.current_price = w_price
                                    
                                    self.detection_label.configure(
                                        text=f"Detected: {common_prediction} = {price} per Kg \nCurrent Weight {total_w}g\nPrice for {total_w}g is ${w_price:.2f}", 
                                        fg='#f39c12'
                                    )

                            
                        else:
                            self.detection_label.configure(text="Looking for food...", fg='#95a5a6')
                            if arduino.in_waiting > 0:
                                total_w = arduino.readline().decode('utf-8').strip()
                                if total_w:
                                    print(f"Received: {total_w}")
                        
                        # Get recommendation if prediction changed
                        if self.last_prediction != common_prediction and common_prediction != "nothing":
                            self.last_prediction = common_prediction
                            # Show "Getting recommendation..." message immediately
                            timestamp = datetime.now().strftime('%H:%M:%S')
                            self.root.after(0, lambda food=common_prediction, ts=timestamp: 
                                self.add_formatted_recommendation(f"🔍 {food.upper()}", "Getting AI recommendation...", "recommendation", ts))
                            self.get_ai_recommendation(common_prediction)

                            
                            
                            
                            
                            
                except Exception as tensor_error:
                    self.update_status(f"Model inference error: {str(tensor_error)}")
                    time.sleep(1)  # Wait before retrying
                    continue
                
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
            except Exception as e:
                self.update_status(f"Detection error: {str(e)}")
                time.sleep(1)  # Wait before retrying
                if not self.is_running:  # Check if we should exit
                    break
    
    def get_ai_recommendation(self, food_item): 
        try:
            # Run AI request in separate thread to prevent GUI freezing
            def ai_request_thread():
                try:
                    prompt_text = (
                        f"Act as a doctor. I have {self.disease}, and "
                        f"I'm considering eating {food_item}. Please tell me if it's good "
                        f"or bad for me, if it good just say good if not kindly suggest a healthier alternative that would "
                        f"satisfy a similar craving or taste.as very short answer in a single line like (its not good for you because it have this content which effects your health condition try this ) and also if the {food_item} is not a food item don't reply anything or just say ok"
                    )
                    
                    payload = {
                        "contents": [
                            {
                                "parts": [{"text": prompt_text}]
                            }
                        ]
                    }
                    
                    response = requests.post(self.url, headers=self.headers, data=json.dumps(payload), timeout=15)
                    
                    if response.status_code == 200:
                        result = response.json()
                        reply = result['candidates'][0]['content']['parts'][0]['text']
                        
                        # Add formatted recommendation to display from main thread
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        def update_gui():
                            self.add_formatted_recommendation(f"🤖 AI RECOMMENDATION - {food_item.upper()}", reply, "recommendation", timestamp)
                        
                        self.root.after(0, update_gui)
                        
                    else:
                        def update_gui_error():
                            self.add_formatted_recommendation(f"❌ ERROR - {food_item.upper()}", f"AI service error (Status: {response.status_code})", "bad")
                        self.root.after(0, update_gui_error)
                        
                except Exception as e:
                    def update_gui_exception():
                        self.add_formatted_recommendation(f"⚠️ ERROR - {food_item.upper()}", f"Network error: {str(e)}", "bad")
                    self.root.after(0, update_gui_exception)
            
            thread = threading.Thread(target=ai_request_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.add_formatted_recommendation(f"❌ ERROR - {food_item.upper()}", f"Request error: {str(e)}", "bad")
    
    def add_recommendation(self, text):
        self.recommendation_text.configure(state='normal')
        self.recommendation_text.insert(tk.END, text)
        self.recommendation_text.see(tk.END)  # Auto-scroll to latest
        self.recommendation_text.configure(state='disabled')
    
    def add_formatted_recommendation(self, title, content, style_type="recommendation", timestamp=None):
        self.recommendation_text.configure(state='normal')
        
        # Add timestamp if provided
        if timestamp:
            self.recommendation_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add title with appropriate styling
        self.recommendation_text.insert(tk.END, f"{title}\n", "food_item")
        
        # Determine content styling based on keywords
        content_lower = content.lower()
        if "good" in content_lower and ("not" not in content_lower or content_lower.index("good") < content_lower.index("not")):
            content_style = "good"
        elif any(word in content_lower for word in ["not good", "bad", "avoid", "harmful", "dangerous"]):
            content_style = "bad"
        else:
            content_style = style_type
        
        # Add content with styling
        self.recommendation_text.insert(tk.END, f"{content}\n", content_style)
        
        # Add separator
        self.recommendation_text.insert(tk.END, "─" * 40 + "\n\n", "separator")
        
        # Auto-scroll to latest
        self.recommendation_text.see(tk.END)
        self.recommendation_text.configure(state='disabled')
    
    def update_camera_display(self):
        if hasattr(self, 'picam2'):
            try:
                # Capture frame
                frame = self.picam2.capture_array()
                
                # Convert to RGB and resize for display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb, (400, 300))
                
                # Convert to PIL Image and then to PhotoImage
                pil_image = Image.fromarray(frame_resized)
                photo = ImageTk.PhotoImage(pil_image)
                
                # Update camera label
                self.camera_label.configure(image=photo)
                self.camera_label.image = photo  # Keep a reference
                
            except Exception as e:
                print(f"Camera display error: {e}")
                # Show error message in camera area
                self.camera_label.configure(image="", text="Camera Error", fg='red')
        
        # Schedule next update
        self.root.after(100, self.update_camera_display)  # Update every 100ms
    
    def on_closing(self):
        self.is_running = False
        if hasattr(self, 'picam2'):
            self.picam2.stop()
        self.root.destroy()

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = FoodRecommendationGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
