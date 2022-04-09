# Park Ranger

My first Capstone project for Springboard's Full-Stack Software Engineering Career Track program.

View this app deployed on [Heroku - Park Ranger](https://park-ranger-mm.herokuapp.com/home)

---

### **Tools Used**

The [National Park Service API](https://www.nps.gov/subjects/developer/api-documentation.htm) was used to make this application. Information on parks all came from this API. 

Styling was achieved by using [Bootstrap V.5.1](https://getbootstrap.com/docs/5.1/getting-started/introduction/) along with overriding inline-styles. 

Other Tools
- Python
- HTML/CSS
- Flask
- SQLAlchemy
- PostgreSQL/SQL
- Flask Bcrypt
- Flask WTForms

---

### **User Flow**

Without registering, users will be able to browse parks via searching by state or by most popular parks in 2021. Users will be able to view all park information on specific park pages and learn about each park.

After registering, users accounts will be saved to the database and now users will have the ability to add parks to a favorites list. They will be able to continue to browse parks and save their favorites to their account, which they can return to and view at a later time. Users will also be able to delete parks from their favorites list, update their information, and delete their accounts if they so choose.

---

### **Using the App Locally (python3 and PostgreSQL required)**

1. Users will need to sign up for an API key from the [National Park Service API](https://www.nps.gov/subjects/developer/api-documentation.htm).
2. Create a file named <i>secret.py</i> on the same level as _app.py_.
3. In the _secret.py_ file, define a variable called **API_SECRET_KEY** and set it equal to your API KEY as a string.

Next, in the terminal, type the following:
1. Navigate to the directory and type `python3 -m venv venv` to create a virtual environment
2. Use that virtual environment by typing `source venv/bin/activate`
3. Install the required dependencies using `pip install -r requirements.txt`
4. Create the local database in PostgreSQL with `createdb NPS_db`
5. Run the __fetch.py__ file to seed the parks table in the database `python3 fetch.py`. This may take a few minutes.
6. Finally, execute the app in the browser with `flask run`

Once complete, users will be able to view the app in their browser on their local port. All functionality will be available to them upon registering for a new account. 
