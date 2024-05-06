# CSE312-Project

domain name: https://cse-project777.us/


Note: If you are testing with docker via following the testing procedure, in the chatroom.html file in public, change the socket line to socket = io({transports:['websocket']});
Note2: Do the same thing with real_ip in server.py where remote_addr is for Docker testing purposes.

<h1>Extra Features</h1>

For objective 3 of part 3, we settled on not just one feature, but two to three additional features to add to our app that aren't part of the requirements of our previous objectives. The two features being: a five-star rating system to our posts, effectively turning them into reviews; and a customizable profile page for each user that doesn't just limit to changing their profile pictures. Users would also be able to view other users' profile pages, though they should be unable to edit them.

<h2>Five-Star Rating</h2>
We added a five-star rating to our posts for posters to practically conduct reviews on certain Anime they watched, giving out their thoughts on them and their final verdict, their overall thoughts simplified through the number of stars they give it. Users can select from 0 to 5 stars, although, to set a post rating to 0 stars would require one to not tamper with the rating system at all.


<h4>Testing Procedure:</h4>

1. Run docker compose up.
2. Navigate to localhost:8080
3. Sign up and log in with your user credentials.
4. Make a post.
5. Check that upon redirecting to your post page, there is an option for you to select your post rating, shown as five black stars.
6. Clicking either of the black stars should set the number of stars depending on which star you clicked on. EX: Clicking on the 5th star should set the rating to five stars.
7. Fill out the required post headers and submit your post.
8. Verify that a post is made with a five-star rating added to it and verify that it matches exactly the rating you've set.
9. Make 5-6 more posts, each with different five star ratings and check if the ratings persist into the newly-created posts.
10. Make a post without setting a rating and ensure that no stars are set to that post upon submitting.


<h2>Customizable Profile</h2>
Registered users are bestowed the ability to customize their own accounts not just limited to their profile pictures. Users would be able to set their user handle, their favorite anime, as well as a description on who they are. In addition, their profile now tracks the number posts they've made.

<h4>Testing Procedure:</h4>

1. Run docker compose up.
2. Navigate to localhost:8080
3. Sign up and log in with your credentials.
4. Click on your icon at the top right of the web app.
5. Verify that you're redirected to a page containing your profile card and its contents, with placeholder text.
6. Also check if your current number of posts is initially 0.
7. Verify that there is a small pen icon next to your username.
8. Check if hoving over it highlights it to a blue color.
9. Check if clicking on it redirects you to a page that allows you to edit your profile card contents, down to your user handle, about me, and your favorite anime.
10. Fill out three sections and submit your changes.
11. Check if your profile card updates as accordingly, maintaining your exact prompts from the edit profile page.
12. Make at least 2 different posts.
13. Navigate back to your profile page and ensure that the post counter on your card matches up with the number of posts you've made.
14. Log out and log back in.
15. Ensure that your new profile changes are kept intact.
16. Restart your docker container.
17. Navigate back to your profile page and check if your profile changes still remain.
18. Log out and make a new account.
19. Navigate back to your profile page, and ensure that the changes made to your previous account don't affect your new account.

<h2>View Others' Profiles</h2>
Users should also be able to view other users' accounts from the posts they make, but should be unable to make changes to those accounts like how they're able to edit theirs.

<h4>Testing Procedure:</h4>

1. Run docker compose up.
2. Open at least three different browers and navigate to localhost:8080.
3. Register and log into three different accounts per browser.
4. Make a post on your first account.
5. Click on your username on your newly-made post.
6. Check if you're redirected back to your own profile page.
7. Check that you're still able to edit your profile, whether by changing your profile picture or editing your card contents.
8. Swap to your 2nd account and make a post there.
9. From your first account, refresh the page and click on the username of the 2nd post made.
10. Check if you're redirected to that user's profile page, but are unable to edit it.
11. From the 2nd account, navigate to the profile page.
12. Ensure that both profile pages match up exactly.
13. From the 2nd account, edit your profile. EX: Changing your profile picture or profile card contents.
14. Refresh your first brower and ensure that the changes made in the 2nd account carry over to its profile page.
15. Likewise, repeat steps 4-14, but swapping the roles of your first account and the second account.
16. Log in to your 3rd account from your 3rd browser.
17. Click on the usernames of both posts made.
18. Check that you're able to view both profile pages, but aren't able to edit them both.
