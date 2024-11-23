from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

DEFAULT_PROFILEPIC = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAYAAACOEfKtAAAACXBIWXMAAAsTAAALEwEAmpwYAAAHJ0lEQVR4nO1ca2wURRxfUYyiiVExmoiJXzUxfiASjB9IlM5caROIpPJMSPwmaoiPiDz0EGhnWt6PUioSoUWhhSYE2o0RpQR7M1t6bSl90Pba8mqEFFoobSmtbcf8d29oRbR3vbvO7rG/5Jdc7ra7M7+dx/811TQXLh56pOTnP4rTSt7GhK1EhBUgymoR5R2YsH4gfEaE1cBvcI2HGtO9XjHhoRcOrTvzCqaMIspbMeUiHCLCrmDKiIcaUx46IT2pp1/AlGUjyvqkIIt3VYq04y0iv6xNnG7qEtXX+kVTx6BJ+Azf5ZW1mdcs3lUxLCRlfYjyrOSN/snawwBE2UJMeDt03pNuiNUFAfFbfae4cGsoZLbcGhInzneKVUcazXtYYrIbCZTP1+IVU7P9ExHle+TI+eynOmFc7AlLuAeRXegRy3LrRkxtvhuepcUTkr3+SZgwHTqYtKFU5PJrEQt3P/f7rorkDaVyWhfBM7V4wNRs/0Qp3tytfnEq0BV18SSLG2+L97eUSREL42IkouC0BfH4hcinbChTelhEnqU5GSidLbKmrRHTkXc/TzbcHp7OaXye5lhThVi7bSzWvNG4z3dV2ovX30srfV5zGjBl2XK3HW/xJJfl1koRMzWneRiIsj6w0aJhqox5PWzpMe1ERPhdR3ksmDIKbx6MZFXiSa483CgNbaI5AV6vmGD5qVz8HqaHEQueqO+UO3IrBC00uwNDVCXo24LLpVpAaMPCTMt3RpRN0+wOTNhKaCw4/arFk1x/rEWOwq81uwNBzI5yM6qiWjjJQ2Vt1jpI2GHN7kCE1UBjIfykWjhJMOKDI/CcZnfgoPEMMTzVwklWX+27Z1RrdgcKBkmb2geVCycZaB+Qoa67mt2BXAEjA3ancIQjkLibSFTMmDwbmTF5ZxxkxmBbGtLNchNZrtkdHmpMt1y5Ctu4cgt2Wq6cJ833luaEYAKm7DI0GFKPqgX89fwtmbG75JhqBkwZgUZD3la1gCuC4SxEeJrmFHioMUUGVCHJo0o8X0u38KRbBnTSevay5iQgyrPgzS87UKds7fs0xwrpY8J3aE5D8kb/ZCi3gA5A0nu8Bfyx5E8ZQGhDm9hzmhORQPl86ASkGCHpPV7iQSQ8KcNKa3oIS9GcDET4bugIJLvHYz30QWJ9673qhJ1afBQVsSIpIiS9YznypHiY8OMzvMWPafGAZK9/khQRpjMkvaO9YcCaJ6ctiBc3xUX3lbeZO7O5O+fWmnnbiKdsS/fwbhuctnEz8h4EqFWByLBVYGkZ21Bg2RJugWV9p2kkwz3kbuv4DSNUQK0KlFuAgStHzqLMCjN7BgkgyGGYJb7tgyZrrvWb30FUBQIDMk0po8xg5znWVIkE4B1Ybp/lO4dHdhncM8d5GDGrZqBsGuRtIWYH2TOIbFsF5KzP/ExYlfkb4cshquKYwIALFy5cuHDhwoULFxFFY9J9czDle8dytDW8I7B8LybGbMdHY7xmetOHMWWHEOF3YiXaf4vJ7yDCDiakGchRXovHysitG+nfeigXS76vFuuKWkVOebcoahoSepQJ94R7wzPgWZ5/+c1sra2POnhSjdcRYTnmMf1gw+ftrDQ7lHeuN+qCjcZDVb1ibWGr+GBH5T8OZ2PC982k/DXNLsCEv4op348IH4BGJqYb4uPcBrHbdzMmIy1sBoZElq9DLM1pMNsWnN4DICS0XZlwKd6axyEyginvNd9wOhefHGgUP5+9o160/xmVX+Y3Cw+Vp9x5LyZ8zQxv8RPjKl5CKnsHEd4k17eluQ0it7xbuUChEtr6UU79yHUyAOdbYi4cnPRBhH2LKf8LHrxg11nxg9GpXJCxco/RafYhKCL06ZuYnWaa4S1+Gk6By+m6+uhlUdg4qFyESHm8cUCsOnpp5Gg8lrDh7FNRFW9WRulLiPByeMCcLX6R5bupvON6lJlV0iFmb5Y5ZVb2bip/MSrizaT+ZzDhlXDjlO0Vtt4k9Ah5sKrXNL3koZwk8sezEYmXsok9iSkvgRsuzKoSR2r6lHdSjzGhj3JdRISdjmiHhiS1WZKxrVyJMawr4uHqu2Lu9nIp4rYxiZdAeSImbGhWhiH2l3cp75Q+ztzn7xKJGQash0PgT4dfhkH4RXgD3xW2Ku+MrohrCq9IX7o5rHIRRHwfynWvKOB8U0UfIwsDg2JBprUeJlC2JDT1hHgEE9YIf7TlZJvyTuiKufmkdUgHEV4f4ugz3pQbB7wB1R3QbTAK5261NpREyt4YVUBM2Qq4+Iu8ZuWN123Cz/Osk06Ysq9CGIH8F7h4+6kbyhuu24TbTl2XHooe8mnLAxU9yhuu2yh6I72TUAQ0ix8L6vqVN1y3CQtqg/8ygPK20QWkbBAuhkiu6obrdmFgSKYEBkcVUOYPlDe6yV6UurgCNrkCCkeMQJf8gRq4AtIYC+jChTae+Bsunp9R/JwoEgAAAABJRU5ErkJggg=="
DEFAULT_EVENTPIC = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEJElEQVR4nO2azWsVVxiHnzQlqdgPESJosAsbsJssbBG6S1bdqhDRxjZtgoUuWt0p/gklZFG6bAWl7kRR3Anix8JUKLXFhXbRQguNkrSFasEWNZEDp3AZzty5M3PnzDuZ3wMHkpkz70zOM+frnYAQQgghhBBCxGdNBUttUPsDqCAha4ZfhNofQIXuQkRcMnuIiIuEGENCmi5Eky79XUVJCKZeKgmhfgkSQouEiHxIiDEkxBgSYgwJMYaEGENCjCEhxpAQY0iIMSSkIMPAEeBb4B9f3M+f+XNFkZACjAI/dMk/3fZ1iiAhORnOkNEppUhPkZCcHMmRqf00b3AJyc+tHEIWC8RXD8nJoxxCXN3WCJkB/gSWgP3YFPKwLUKOAasd93gK7CUOGrI6GAA+T3kbHwOTEYS4fYYmdWAQ+DqjMf4GdlUsZNgvaXtZ9g6t1yHLNcL5QOwngWMPgDGqZTRDyrreGL4CXEnpDZPAQuDcL8BWqmXI7zMW/UTvyk1/rEjPaISQzf4PTsZ0q6t3OuaVk4E6d/z1TcOskG2+UZPxfgV2BuaXc4G6TuZGmoVJIW/6hk/GugtsT7lmA3AjcM0l4EWagzkhbwPLgTjfASMZ174GfB+49gzwAs3AlJBJP1knY1wFXu0xxhbgp0CML2kGZoTs8Zu75PUXgZdy/lFvAPcDsY5jHxNCZlL2FKdLjP/jwF+JeC7dchjb1C7kaCIv9X/5wi9pyzAR6HUu7zWFXWoT4hp7PlB/1ScP+8VeL6HzHo+9rDJMAyvA78BBGi7E7Ru+CtR1Dfcx/eeDQC90i4e3CsabBZ4lXqJPmirE5aXOBur9V/F3jeOBey4HNpl5ZfRbSlQhLwOXA3Xcv9C8S/XMl8x7pcnop5RoQkb85i553o3Du4nDAHAq8Aw/Apsyrp0LyHiWcszVNS3kdeBe4NySX57GZLBA3ivUM9zvH6WcK9NTKhfi8lK/BY7/DOygHjYA13vMe6XJ+DCjTlEplQv5o2Beqmo2+aEq+WynOvY/oWHqqV+19TqkzVkTkizXcuSlqmZLl7zXbIoMl1VIox89JaqQCwXyUlUz5j/7Jp91NSDDbQazKNtTogn5xvB3ifFA3isp4/0c8cr0lChCFvqQl6qaCeDfwLO7pOeBAvGK9pTKhZygGcwFGvBJyexBESmVC2myjKmKYneT0nohsymrqV4m8CrmlFYLmU2RcSjSvUJSWitkOkLPKDJ8tVLIQCCDkLYDjy2ltUJWuuSm6pTSSiGOfV6K+0j1HvFJk9JaIRYISZGQmsn6CplEPaRmKUkkpObhK4mERKTVqyyrSIgxJMQYEmIMCWmbEBVKtYGEYOslkhDqlyAhrGMholokxBgSYgwJaZoQFeqd9CUAU21Q+wOoICFrhl8EIYQQQgghhCAmzwFP3jk+Vt9ergAAAABJRU5ErkJggg=="

event_list = []
user_list = []
possible_intersts = [
    'Bouldering',
    'Hiking',
    'Pub Crawls',
    'Chess',
    'Picnics',
    'Museums', 
    'Boccia',
    'Running',
    'Board Games'
]

class Event:

    def __init__(self, event_title, event_description, event_picture, event_date, event_location, event_host):
        self.id = str(uuid.uuid4())
        self.title = event_title
        self.description = event_description
        self.picture = event_picture
        self.event_date = event_date
        self.create_date = datetime.now()
        self.location = event_location
        self.host = event_host
        self.visitors = []

class User:

    def __init__(self, user_name, user_profilepic, user_dateofbirth, user_interests, user_email):
        self.id = str(uuid.uuid4())
        self.username = user_name
        self.profilepic = user_profilepic
        self.dateofbirth = user_dateofbirth
        self.interests = user_interests
        self.email = user_email
        self.events = []

@app.route('/create_event', methods=['POST'])
def create_event():
    try:
        # Parse JSON data from the request
        data = request.get_json()

        # Set default values for attributes
        title = data.get('title', 'Untitled Event')
        description = data.get('description', 'No description provided')
        picture = data.get('picture', DEFAULT_EVENTPIC)
        date = data.get('date', None)
        latitude = data.get('latitude', 0.0)
        longitude = data.get('longitude', 0.0)
        host = data.get('host', 'Anonymous')


        # Create a new Event object
        new_event = Event(title, description, picture, date, [latitude, longitude], host)

        # Add the event to the event_list
        event_list.append(new_event)

        # Return the event_id
        return jsonify({'event_id': new_event.id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_event', methods=['PUT'])
def update_event():
    try:
        # Parse JSON data from the request
        data = request.get_json()

        # Check if an id was given
        if 'event_id' not in data:
            return jsonify({'error': 'No event specified'}), 400
        else:
            for element in event_list:
                if element.id == data.get('event_id'):
                    event = element
                    break
        
        # Update the given attributes
        if 'title' in data:
            event.title = data.get('title')
        if 'description' in data:
            event.description = data.get('description')
        if 'picture' in data:
            event.picture = data.get('picture')
        if 'date' in data:
            event.event_date = data.get('date')
        if 'latitude' in data:
            event.location[0] = data.get('location')
        if 'longitude' in data:
            event.location[1] = data.get()
        if 'host' in data:
            event.host = data.get('host')

        # Return the event_id
        return jsonify({'event_id': event.id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/delete_event', methods=['DELETE'])
def delete_event():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        
        for event in event_list:
            if event.id == data.get('event_id'):
                event_list.remove(event)
                return jsonify({'event_id': event.id}), 200
        return jsonify({'error': 'Event not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        # Parse JSON data from the request
        data = request.get_json()

        # Set default values for attributes
        name = data.get('name', 'Anonymous')
        profilepic = data.get('profilepic', DEFAULT_PROFILEPIC)
        dateofbirth = data.get('dateofbirth', None)
        interests = data.get('interests', [])
        email = data.get('email', 'No email specified')

        # Create a new Event object
        new_user = User(name, profilepic, dateofbirth, interests, email)

        # Add the event to the event_list
        user_list.append(new_user)

        # Return the user_id
        return jsonify({'user_id': new_user.id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_user', methods=['PUT'])
def update_user():
    try:
        # Parse JSON data from the request
        data = request.get_json()

        # Check if an id was given
        if 'user_id' not in data:
            return jsonify({'error': 'No user specified'}), 400
        else:
            for element in user_list:
                if element.id == data.get('user_iid'):
                    user = element
                    break
        
        # Update the given attributes
        user.name = data.get('name', user.name)
        user.profilepic = data.get('profilepic', user.profilepic)
        user.date = data.get('date', user.date)
        user.location = data.get('location', user.location)
        user.host = data.get('host', user.host)
        user.interests = data.get('interests', user.interests)
        user.email = data.get('email', user.email)

        # Return the user_id
        return jsonify({'user_id': user.id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        
        for user in user_list:
            if user.id == data.get('user_id'):
                user_list.remove(user)
                return jsonify({'user_id': user.id}), 200
        return jsonify({'error': 'User not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/join_event', methods=['POST'])
def join_event():
    try:
        data = request.get_json()
        for user in user_list:
            if user.id == data.get('user_id'):
            
                for event in event_list:
                    if event.id == data.get('event_id'):
                        
                        if event.id in user.events or user.id in event.participants:
                            return jsonify({'error': 'User already joined the event'}), 409
                        else:
                            user.event.append(event.id)
                            event.participants.append(user.id)
                            return jsonify({'event_id': event.id,'participants': event.participants}), 200
                return jsonify({'error': 'Event not found'}), 404
        return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@app.route('/get_interests', methods=['GET'])
def get_interests():
    return jsonify(possible_intersts)

print('Success')