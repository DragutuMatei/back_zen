from django.core.files import File
from copy import copy
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import json 
from django.http import JsonResponse
from firebase_admin import db, auth, storage
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from .models import Another
from .serializers import AnotherSerializer, YourModelSerializer 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from back.settings import database, storage, auth
from rest_framework.authentication import get_authorization_header
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


@api_view(['POST']) 
def create_data(request):
    serializer = YourModelSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        # # print(data)
        firebase_data = {
            'field1': data['field1'],
            'field2': data['field2'],
        }
        
        root_ref = db.reference('/')

        new_ref = root_ref.child('maybe').push(firebase_data)

        document_id = new_ref.key

        # Return the ID of the inserted data
        return Response({'id': document_id}, status=status.HTTP_201_CREATED)

        # collection_ref = db.collection('your_collection_name')
        # ok, bn = collection_ref.add(firebase_data)
        # # # print(ok)
        # # # print(bn.id)

        # doc_data = dir(bn)

        # # # print(doc_data)

        # return Response({'id': bn.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_object_by_id(request, object_id):
    root_ref = db.reference('/')
    object_ref = root_ref.child('your_collection_name').child(object_id)

    object_data = object_ref.get()

    if object_data:
        return JsonResponse(object_data, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_all_objects(request):
    root_ref = db.reference('/')
    collection_ref = root_ref.child('your_collection_name')

    all_objects = collection_ref.get()

    if all_objects:
        return JsonResponse(all_objects, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'No objects found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_object_by_id(request, object_id):
    serializer = YourModelSerializer(data=request.data)
    
    if serializer.is_valid():
        data = serializer.validated_data

        root_ref = db.reference('/')
        object_ref = root_ref.child('your_collection_name').child(object_id)

        object_ref.update({
            'field1': data['field1'],
            'field2': data['field2'],
            # Map other fields accordingly
        })

        return JsonResponse({'message': 'Object updated successfully'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TODO: sa nu duplic fisierele in storage 


@api_view(['POST'])
def login_or_register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Check if the user exists in the Django database
    user = authenticate(request, username=email, password=password)

    if user is not None:
        # User exists, log in
        login(request, user)
        return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        # User does not exist, register in Firebase
        try:
            # Create user in Firebase (this is just an example, adjust as needed)
            firebase_user = auth.create_user(
                email=email,
                password=password
            )

            # Create user in Django database
            new_user = User.objects.create_user(username=email, email=email, password=password)

            # Log in the newly registered user
            login(request, new_user)

            return Response({'detail': 'Registration and login successful'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return Response({'detail': 'Logout successful'}, status=200)

@api_view(['POST']) 
def create_data_with_img(request):
    # # print(request.data)
    # Assuming YourModelSerializer supports multiple file uploads
    # serializer = AnotherSerializer(data=request.data)
    # # # print(serializer.is_valid())
    
    # if serializer.is_valid():
        # data = serializer.validated_data
        # # # print(data)
    firebase_data = {
        'title': request.data['title'],
        'description': request.data['description'],
        # Map other fields accordingly
    }

    # # print(request.data['files'])
    # Handle file uploads
    files = request.data['files']
    file_urls = []
    # for file in files:
        # # print(file)
        
    # for file in files:
    #     # Upload each file to Firebase Storage
    #     storage_ref = storage.bucket(name="Django").blob(file.name)
    #     storage_ref.put(file)

    #     # Get the URL of the uploaded file
    #     file_url = storage_ref.get_url()  # Assuming you have a method to get the URL (check Firebase Storage documentation)
    #     file_urls.append(file_url)

    # # Add file URLs to the Firebase data
    # firebase_data['file_urls'] = file_urls

    # Push data to the Realtime Database
    root_ref = db.reference('/')
    new_ref = root_ref.child('coaie').push(firebase_data)
    document_id = new_ref.key

    # Return the ID of the inserted data along with file URLs
    return Response({'id': document_id, 'file_urls': file_urls}, status=status.HTTP_201_CREATED)
    # # # print("nu e ok")
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST']) 
def upload_images(request):
    # Get the images from the request
    # # print(request.FILES)
    images = request.FILES.getlist('images')
    # # print(images)
    # Upload each image to Firebase
    for image in images:
        file = File(image)
        filename = image.name

        # Save the image to Firebase Storage
        storage.FirebaseStorage.instance().child('images').child(filename).put(file)

        # Get the download URL of the image
        download_url = storage.FirebaseStorage.instance().child('images').child(filename).get_url(
            download=True
        )

        # Send the download URL back to the client
        return JsonResponse({'download_url': download_url})
    
    
@api_view(['GET'])
def getIt(request):
    data = database.child('da').get().val()
    return JsonResponse( data, safe=False) 
    
@api_view(["POST"])
def testIt(request):
    # # print(request.data['images'])
    
    path = f"images/{request.data['images']}"
    
    # upload:
    storage.child(path).put(request.data['images'])
    
    # get link
    link = storage.child(path).get_url(None)
    # # print(link)    
    
    # # # print(str(request.data))
    # # # print(request.FILES)
    # # # print(str(request))
    
    # for image in request.data['images']:
    #     # # print(image)
    
    return Response({'link': link}, status=status.HTTP_201_CREATED)
    
    
class Teste(viewsets.ModelViewSet):
    queryset = Another.objects.all()
    serializer_class = AnotherSerializer
    
class Idk(APIView):
    permission_classes= [permissions.AllowAny]

    def get(self, request):
        
        token = get_authorization_header(request)
        token = str(str(token[6:])[2:-1])
        # # # print(token[6:].index('b'))
        # # print('eyJhbGciOiJSUzI1NiIsImtpZCI6IjAzMmNjMWNiMjg5ZGQ0NjI2YTQzNWQ3Mjk4OWFlNDMyMTJkZWZlNzgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZGphbmdvLTI1NDZhIiwiYXVkIjoiZGphbmdvLTI1NDZhIiwiYXV0aF90aW1lIjoxNzAzNDU3MjIwLCJ1c2VyX2lkIjoiR2xXT2dVVG40dGZzc0FEOVBPa25seVJuZ1N4MSIsInN1YiI6IkdsV09nVVRuNHRmc3NBRDlQT2tubHlSbmdTeDEiLCJpYXQiOjE3MDM0NTcyMjAsImV4cCI6MTcwMzQ2MDgyMCwiZW1haWwiOiJtYXRlaWRyN0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsibWF0ZWlkcjdAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.RO1BvbZvUCalLQzXfNRrAbVVzZ4M25XzIL5w2GSd6lUYTlAtlWBQnHGM16u30A_tYmvms7bVXJ9O2bgyK-b_sGY343M6Jofh6g0TJUS4RO0NgjI0IWL-OC3VUNpYS1pQiXHzwnUmXKaIST3E6IVGgDZJd1EU5cF42YrR9i6GyiD9FRekC9YP29vcdOA5EXridADu0bX0Sdd3VWLwqmdfscno8POS8Ma7WxII2Nu-aOVF-6zohjQ95R-tRz24AgzZTwmtzpY9se4GCRFhNIxDqlyYjUUNkTUYKKF_UN2FoG_oFcBByOxuDiqbUM8QNIsAysA92-H5xEV-Rem6MBfDQw')
        # # print('\n')
        # # print(type(token))
        # # print('\n')
        # # print(token)
        # # print('\n')
        # # print('\n')
        # # # print(auth.get_account_info('eyJhbGciOiJSUzI1NiIsImtpZCI6IjAzMmNjMWNiMjg5ZGQ0NjI2YTQzNWQ3Mjk4OWFlNDMyMTJkZWZlNzgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZGphbmdvLTI1NDZhIiwiYXVkIjoiZGphbmdvLTI1NDZhIiwiYXV0aF90aW1lIjoxNzAzNDU3MjIwLCJ1c2VyX2lkIjoiR2xXT2dVVG40dGZzc0FEOVBPa25seVJuZ1N4MSIsInN1YiI6IkdsV09nVVRuNHRmc3NBRDlQT2tubHlSbmdTeDEiLCJpYXQiOjE3MDM0NTcyMjAsImV4cCI6MTcwMzQ2MDgyMCwiZW1haWwiOiJtYXRlaWRyN0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsibWF0ZWlkcjdAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.RO1BvbZvUCalLQzXfNRrAbVVzZ4M25XzIL5w2GSd6lUYTlAtlWBQnHGM16u30A_tYmvms7bVXJ9O2bgyK-b_sGY343M6Jofh6g0TJUS4RO0NgjI0IWL-OC3VUNpYS1pQiXHzwnUmXKaIST3E6IVGgDZJd1EU5cF42YrR9i6GyiD9FRekC9YP29vcdOA5EXridADu0bX0Sdd3VWLwqmdfscno8POS8Ma7WxII2Nu-aOVF-6zohjQ95R-tRz24AgzZTwmtzpY9se4GCRFhNIxDqlyYjUUNkTUYKKF_UN2FoG_oFcBByOxuDiqbUM8QNIsAysA92-H5xEV-Rem6MBfDQw'))
        user = auth.get_account_info(token)
        email = user['users'][0]['email'] 
        details = database.child("users").order_by_child("user_email").equal_to(email).get().val()
        user_id = list(details.keys())[0]
        more = details[user_id]
        user['premium'] = False
        user['plan'] = more['plan']
        user['user_email'] = more['user_email']
        user['meditations'] = more['meditations']
        user['sounds'] = more['sounds']
        user['yogas'] = more['yogas']
        if 'time' in more:
            # print(more)
            # print("are")
            if int(datetime.now().timestamp()) < int(more['time']):
                # print("are premium")
                user['premium'] = True
            else:
                # print("NU are premium")
                user['premium'] = False
        else:
            user['premium'] = False
            # print("NU are premium")
        
        combined_dict = user 


        return Response({"user": combined_dict})

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if "matei" in email:
            try:
                user_l = auth.sign_in_with_email_and_password(email, password)
                
                user = auth.get_account_info(user_l['idToken'])
                email = user['users'][0]['email'] 
                details = database.child("users").order_by_child("user_email").equal_to(email).get().val()
                user_id = list(details.keys())[0]
                more = details[user_id]
                user['premium'] = False
                user['plan'] = more['plan']
                user['user_email'] = more['user_email']
                user['meditations'] = more['meditations']
                user['sounds'] = more['sounds']
                user['yogas'] = more['yogas']
                if 'time' in more:
                    # print(more)
                    # print("are")
                    if int(datetime.now().timestamp()) < int(more['time']):
                        # print("are premium")
                        user['premium'] = True
                    else:
                        # print("NU are premium")
                        user['premium'] = False
                else:
                    user['premium'] = False
                    # print("NU are premium")
                
                combined_dict = user 
                return Response({'token': user_l['idToken'], "admin":True, 'user':user})
            except:
                return Response({'error':"Invalid credentials"})
            # print("e din pagina de admin!!!!!!!!!!")
        else:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                token = user['idToken']
                return Response({'token': token, "admin": False})        
            except:
                return Response({'error':"Invalid credentials"})
                
            
    def register(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        print(email, password)
        
        return Response({"data":False})    
        

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request, *args, **kwargs):
        # # print(self.request.user)
        try:
            user = auth.verify_id_token(request.auth)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=403)
        
class UpdateUsers(viewsets.ViewSet):
    def updateTime(self, request):
        email = request.data["email"] 
        plan = request.data["plan"] 
        
        curent_user_timestamp = database.child("users").order_by_child("user_email").equal_to(email).get().val()
        
        # print(curent_user_timestamp)
        
        user_id = list(curent_user_timestamp.keys())[0]
        # user = curent_user_timestamp[meditation_id]
        # print(user)

        months_to_add = int(plan)

        future_timestamp = (datetime.now() + relativedelta(months=months_to_add)).timestamp()
        
        print(future_timestamp)

        database.child("users").child(user_id).update({'time': future_timestamp})
        
        return Response({"data":True}, status=status.HTTP_200_OK)
    
    def register(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        print(email, password)
        

        try:
            newuser = auth.create_user_with_email_and_password(email, password)

            print(newuser)

            token = newuser['idToken']
            database.child('users').push({"user_email": newuser['email'], 'meditations':0, 'sounds':0, 'yogas':0 })            
            return Response({'token': token, "admin": True})  
        except:
            return Response({"error":"Invalid credentials"})
        # return Response({"data":False})
            
            

class Meditations(viewsets.ViewSet):
    def create(self, request):
        path = f'meditations/back/{request.data["background"]}'
        path2 = f'meditations/mp3s/{request.data["mp3"]}'

        storage.child(path).put(request.data["background"])
        storage.child(path2).put(request.data["mp3"])

        background = storage.child(path).get_url(None)
        mp3 = storage.child(path2).get_url(None)

        data = copy(request.data)
        data['background'] = background
        data['mp3'] = mp3

        data2 = MeditationSerializer(data = data)
        if data2.is_valid():
            data3 = copy(data2.data)
            data3['tags'] = copy(data3['tags'][0].split(','))
            result = database.child("meditations").push(data3)
            return Response({"id": result['name'], "data":data3}, status=status.HTTP_201_CREATED)
        else: 
            print(data2.errors)
            print(data2.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        data = database.child("meditations").order_by_child("createdAt").get().val()
        return Response({"data":data}, status=status.HTTP_200_OK)
            
    def destroy(self,request, pk=None):
        print(pk)
        print(database.child("meditations"))
        database.child("meditations").child(pk).remove()
        return Response({"data":True}, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        print(pk)
        meditation = database.child("meditations").order_by_child("createdAt").equal_to(pk).get().val()

        print(meditation)
        return Response({'data':meditation}, status=status.HTTP_200_OK)
    
    def get_by_cat(self, request, pk=None):
        print(pk)
        meditation = database.child("meditations").order_by_child("category").equal_to(pk).get().val()
        print(meditation)
        return Response({'data':meditation}, status=status.HTTP_200_OK)
    
    def updateCountMed(self, request):
        email = request.data['email']
        user = database.child("users").order_by_child("user_email").equal_to(email).get().val()
        print("users: ", user)
        user_id = list(user.keys())[0]
        if 'meditations' not in user[user_id]:
            new_med = 1
        else:
            new_med = int(user[user_id]['meditations']) + 1
        database.child("users").child(user_id).update({'meditations': new_med})
        return Response({'user':user})

 
# class Cards(viewsets.ViewSet):
#     def create(self, request):
#         back_path = f'cards/back/{request.data["background"]}'
#         mp3_path = f'cards/mp3s/{request.data["mp3"]}'
        
#         storage.child(back_path).put(request.data['background'])
#         storage.child(mp3_path).put(request.data['mp3'])
        
#         background = storage.child(back_path).get_url(None)
#         mp3 = storage.child(mp3_path).get_url(None)
        
#         data = copy(request.data)
#         data['background'] = background
#         data['mp3'] = mp3
        
#         ser_data = CardSerializer(data = data)
#         if ser_data.is_valid():
#             result = database.child("cards").push(ser_data.data)
#             return Response({"id":result['name'], 'data':data}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
            
            
#     def list(self, request):
#         data = database.child('cards').order_by_child("createdAt").get().val()
#         return Response({'data':data}, status=status.HTTP_200_OK)
    
#     def destroy(self,request, pk=None):
#         # # print(pk)
#         database.child("cards").child(pk).remove()
#         return Response({"data":True}, status=status.HTTP_200_OK)    
    
#     def retrieve(self, request, pk=None):
#         card = database.child('cards').order_by_child("createdAt").equal_to(pk).get().val()
#         return Response({'data':card}, status=status.HTTP_200_OK)

class Sounds(viewsets.ViewSet):
    def getCategories(self, request):
        data = database.child('categ_sounds').get().val()        
        return Response({'data':data}, status=status.HTTP_200_OK)

    def create(self, request):
        back_path = f'sounds/back/{request.data["background"]}'
        thumb_path = f'sounds/thumb/{request.data["thumbnail"]}'
        mp3_path = f'sounds/mp3s/{request.data["mp3"]}'
        
        storage.child(back_path).put(request.data['background'])
        storage.child(thumb_path).put(request.data['thumbnail'])
        storage.child(mp3_path).put(request.data['mp3'])
        
        background = storage.child(back_path).get_url(None)
        thumbnail = storage.child(thumb_path).get_url(None)
        mp3 = storage.child(mp3_path).get_url(None)
        
        data = copy(request.data)
        data['background'] = background
        data['thumbnail'] = thumbnail
        data['mp3'] = mp3
        
        ser_data = SoundSerializer(data=data)
        if ser_data.is_valid():
            result = database.child("sounds").push(ser_data.data)
            return Response({"id":result['name'], 'data':data}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
    def list(self, request):
        data = database.child('sounds').order_by_child("createdAt").get().val()
        return Response({'data':data}, status=status.HTTP_200_OK)

    def destroy(self,request, pk=None):
        # # print(pk)
        database.child("sounds").child(pk).remove()
        return Response({"data":True}, status=status.HTTP_200_OK)    
        
    def retrieve(self, request, pk=None):
        sound = database.child('sounds').order_by_child("createdAt").equal_to(pk).get().val()
        return Response({'data':sound}, status=status.HTTP_200_OK)

    def get_by_cat(self, request, pk=None):
        print(pk)
        meditation = database.child("sounds").order_by_child("category").equal_to(pk).get().val()
        print(meditation)
        return Response({'data':meditation}, status=status.HTTP_200_OK)
    
    def updateCountSound(self, request):
        email = request.data['email']
        user = database.child("users").order_by_child("user_email").equal_to(email).get().val()
        print("users: ", user)
        user_id = list(user.keys())[0]
        if 'sounds' not in user[user_id]:
            new_med = 1
        else:
            new_med = int(user[user_id]['sounds']) + 1
        database.child("users").child(user_id).update({'sounds': new_med})
        return Response({'user':user})
    
class Yoga(viewsets.ViewSet):
    
    def create(self, request):
        path = f'yoga/{request.data["mp4"]}'
        back_path = f'yoga/back/{request.data["background"]}'
        
        storage.child(path).put(request.data['mp4'])
        storage.child(back_path).put(request.data['background'])
        
        mp4 = storage.child(path).get_url(None)
        background = storage.child(back_path).get_url(None)
        
        data = copy(request.data)
        data['mp4'] = mp4
        data['background'] = background
        
        ser_data = YogaSerializer(data = data)
        
        if ser_data.is_valid():
            result = database.child('yoga').push(ser_data.data)
            return Response({"id":result['name'], 'data':data}, status=status.HTTP_201_CREATED)
        else:        
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        data = database.child('yoga').order_by_child("createdAt").get().val()
        return Response({'data':data}, status=status.HTTP_200_OK)
    
    def destroy(self,request, pk=None):
        # # print(pk)
        database.child("yoga").child(pk).remove()
        return Response({"data":True}, status=status.HTTP_200_OK)
        
    def retreive(self, request, pk=None):
        breath = database.child('yoga').order_by_child("createdAt").equal_to(pk).get().val()
        return Response({'data':breath}, status=status.HTTP_200_OK)
    
    def updateCountYoga(self, request):
        email = request.data['email']
        user = database.child("users").order_by_child("user_email").equal_to(email).get().val()
        print("users: ", user)
        user_id = list(user.keys())[0]
        if 'yogas' not in user[user_id]:
            new_med = 1
        else:
            new_med = int(user[user_id]['yogas']) + 1
        database.child("users").child(user_id).update({'yogas': new_med})
        return Response({'user':user})

class Podcast(viewsets.ViewSet):
    
    def create(self, request):
        path = f'podcast/{request.data["mp4"]}'
        back_path = f'podcast/back/{request.data["background"]}'
        
        storage.child(path).put(request.data['mp4'])
        storage.child(back_path).put(request.data['background'])
        
        mp4 = storage.child(path).get_url(None)
        background = storage.child(back_path).get_url(None)
        
        data = copy(request.data)
        data['mp4'] = mp4
        data['background'] = background
        
        ser_data = PodcastSerializer(data = data)
        
        if ser_data.is_valid():
            result = database.child('podcast').push(ser_data.data)
            return Response({"id":result['name'], 'data':data}, status=status.HTTP_201_CREATED)
        else:        
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        data = database.child('podcast').order_by_child("createdAt").get().val()
        return Response({'data':data}, status=status.HTTP_200_OK)
    
    def destroy(self,request, pk=None):
        # # print(pk)
        database.child("podcast").child(pk).remove()
        return Response({"data":True}, status=status.HTTP_200_OK)
        
    def retreive(self, request, pk=None):
        breath = database.child('podcast').order_by_child("createdAt").equal_to(pk).get().val()
        return Response({'data':breath}, status=status.HTTP_200_OK)

