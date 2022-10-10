from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from sensor_msgs.msg import Image
from std_msgs.msg import Int16, Int32MultiArray
from cv_bridge import CvBridge
import rospy

product_name = ['Blue_Bottle', 'Chocolate', 'Clock', 'Color_Nail', 'Fish', 'Pink_Bottle', 'Remover', 'Round_Bread', 'Square_Bread', 'Sweet_Potato', 'Tomato', 'Toothpaste', 'Wet_Tissue']
product_price = [3000, 1000, 3500, 1500, 4000, 3000, 2000, 3200, 3800, 4500, 4800, 2000, 2000]

total_price = 0
products = []
object_list = []


class LoginView(auth_views.LoginView):
    template_name = "main/login.html"
    redirect_authenticated_user = True

login = LoginView.as_view()
logout = auth_views.LogoutView.as_view()

def main(request):
    return render(request, 'main/main.html', {'products': products, 'total': total_price})

class SubscribeTester:
    def __init__(self):
        self.cv_bridge = CvBridge()
        detectron_topic = '/detectron_img'
        object_label_topic = '/object_labels'
        _image_sub = rospy.Subscriber(detectron_topic, Image, self._rgb_callback)
        _image_sub2 = rospy.Subscriber(object_label_topic, Int32MultiArray, self._object_label_callback)

    def _rgb_callback(self, img_msg):
        self.cv_image = self.cv_bridge.imgmsg_to_cv2(img_msg, 'passthrough')
        #cv2.imshow('detecron_img', self.cv_image)
        #cv2.waitKey(1)

    def _object_label_callback(self, data):
        self.object_label_list = list(data.data)
        for i in self.object_label_list:
            if i not in object_list:
                object_list.append(i)
                products.append([product_name[i], 1, product_price[i], product_price[i]])
                global total_price
                total_price += product_price[i]
                print(products)
class VideoCamera(object):
    def __init__(self):
        self.frame = subscribe_tester.cv_image
        threading.Thread(target=self.update, args=()).start()
    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    def update(self):
        while True:
            self.frame = subscribe_tester.cv_image

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def camera(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")
        pass

rospy.init_node('ui_image_ros_subscriber')
subscribe_tester = SubscribeTester()