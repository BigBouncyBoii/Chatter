# Web application called Chatter

## Distinctiveness and Complexity

This web application is a real time messaging app which also combines the explorability of social media. 
Users can access 3 types of chats which is a global chat with all users, public group chats with multiple users, and direct chats between individuals. 

The real time messaging feature which has been created is a distinct and much more complex feature when compared to previously implemented features from previous projects. This is because the messaging feature had to be designed with a backend API which continously handled web requests and a front-end which detected had to detect any changes and dynamically generate messages. Overall, this gives a user the sense of real-time chat messaging. 
Moreover, profile pictures have also been implemented into Chatter, a feature which is distinct from previous projects. The feature of infinite scroll on the front end has also been implemented to give user's a text-messaging app experience. 
A group invite and friend request system has also increased the complexity of this project. 
Lastly, this project is more complex than previous projects because it has utlized 9 models and 28 views, much more than previous projects

## Explaining the types of chats more in depth + how to run the application 

General chat features:
Messages are generated in real time which means that a user will receive a message from another user as soon as it is sent without having to reload their page. This was achieved with a set interval javascript function which requested the django API for messages stored in the database every 500ms, a short enough time span to give a sense of "real time". After the request, the id of each new message (and the likes as well) received from the API was checked against the id of each old message displayed on the webpage. If the IDS did not match, the messages would be updated dynamically. For a user to send a message, the message would be sned via a POST request asynchronously to the API. Users could also like messages which was implemented by a PUT request, and reply to messages which functioned the same was as regularly sending a message but with the message being replied to saved as well. The messages were dynamically generated to color all messages sent by the user yellow and all messages sent by other users grey. Users, when reading messages, can scroll up to generate previously sent messages. 

Global chat:
All users can access this chat with one catch. There is a messaging cooldown of one day (to prevent spam). The global chat is also the index of the web application. 

Group chat:
Users can create group chats with a category and description of the group chat. To join a group chat, the users can use the search feature and join the group chat, users can also find recently made groups in the group chat home page, or users can be invited to the group chat and accept the invite through their profile page. 

Direct chats: 
Users who are friends can directly message each other. To be friends, a friend request had to be sent and accepted. Users can send a friend request by clicking on a username, being taken to their profile page and requesting to be friends. Friend request can be accepted through a user's profile page or by going to the profile of the user who sent a friend request and sending them a friend request as well. 

## Other features 
Profile pictures:
Users can upload a profile picture (and a bio) to their profile. This was acheived by creating a seperate model connected to the main User model which had an image field. Also, the upload of profile pictures to the server is controlled by a django form. 

Style:
CSS was used, but bootstrap was also used for style and font awesome was used for icons 

## What is contained in each file
requirements.txt - Pillow had to be installed for images to work
views.py - contains the views which directs the users around the website and handles group invites, searches, friend requests and much more. Also contains the API which handles the continous web requests from global, group and direct chats. 
urls.py - Contains all the routes (as well as API routes) of the web application 
models.py - contains all the models which are used in the web application. There are 2 models for the user and profile picture, a model which stores the global messages, 3 models which stores group invites, created groups and group messages, 3 models which store friend requests, friends, and direct messages. 
chatter.css - This contains the CSS used to style the webpage.
images folder - this contains the general images used in the  (such as the logo)
profile_picture folder - this contains the profile pictures which have been uploaded to the website to be displayed 
direct_home.html - this displays all the friends and corresponding direct chats the user has with that friend 
direct.html - this displays the actual direct chat and contains the javascript for requesting and updating chat messages 
group_home.html - this displays recently created groups as well as the groups which the user has joined 
group.html - this displays the actual group chat and contains the javascript for requesting and updating chat messages 
index.html - this displays a login page for users who are not logged in and the global chat for users who are logged in. 
layout.html - this contains the general structure of a page, as well as the navbar
profile.html - this displays the profile of a user. If the user is yourself, you can make changes to your profile picture and bio as well as accept and reject friend requests and group invites. 
register.html - for user's to register themselves
search.html - to search for groups and users 

## Note
In hindsight, I should have written my javascript code in seperate files to maintain neatness. 


