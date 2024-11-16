# Porygon Autonomous Chat VideoGenerator

 <img src="assets/porygon-logo.png" align="right" width="200" height="200" alt="Porygon Logo">

I would like to build an automated content generation AI that does the following:
1. Generate scenarios
   - Create dynamic conversations between two people
   - Develop engaging storylines
   - Ensure natural dialogue flow

2. Reflect content into designs
   - Place text into provided message bubbles
   - Adjust content to fit design templates
   - Maintain visual consistency

3. Create video content
   - Sequence screenshots in proper order
   - Add synchronized sound effects
   - Ensure smooth transitions

4. Upload to social platforms
   - Post to TikTok
   - Share on Instagram
   - Monitor upload status

I want this pipeline to work on two different apps in two different categories, we can meet to discuss the requirements. Only apply if you are confident you have the skills for that and can achieve it within 2 weeks max

### Setting up the project

Clone the project
```
git clone https://github.com/millionairemacmillionairemac/ai-generated-text-convo-video.git
```

Run the following command to install python dependencies in the backend folder
```
cd backend && pip install -r requirements.txt
```

### Setting Up

We'll be working with

- Google Cloud and Google Cloud Storage
- TikTok API
- Instagram API

#### Getting a service account json key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to the "IAM & Admin" section
3. Click on "Service Accounts"
4. Click on "Create Service Account"

#### Creating a Google Cloud Storage bucket

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to the "Storage" section
3. Click on "Create Bucket"
4. Fill out the required information and click on "Create"

#### Creating a developer account on TikTok

1. Go to the [TikTok Developer Portal](https://developers.tiktok.com/en) and log in with your TikTok account
2. Click on "Create App"
3. Fill out the required information and click on "Create"
4. In the sidebar on the left, click on "Settings"
5. In the "OAuth" tab, click on "Add"
6. Add `https://localhost:8000/redirect` as the "OAuth redirect URI"
7. Make sure "Access Token" is enabled
8. Click on "Save"

#### Creating a developer app with your instagram account and getting an access token

1. Go to the [Instagram Developer Portal](https://developers.facebook.com/apps/) and log in with your Facebook account
2. Click on "Create"
3. Fill out the required information and click on "Create"
4. In the sidebar on the left, click on "Settings"
5. In the "Valid OAuth redirect URIs" field, add `https://localhost:8000/redirect`
6. In the sidebar on the left, click on "Products"
7. Click on "Add Product" and select "Instagram"
8. In the sidebar on the left, click on "Tools"

#### We'll need to take all of the information you just created and put it in the `backend/.env` file 

In the root of the project with the following names (case sensitive):

- TIKTOK_CLIENT_KEY
- TIKTOK_CLIENT_SECRET
- TIKTOK_REDIRECT_URI
- OPENAI_API_KEY
- INSTAGRAM_TOKEN

