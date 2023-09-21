from flask import Flask, redirect,request
from flask_restful import Resource, Api
from user_agents import parse
import sys
from models.connection import DBConnection
import uuid
import requests

app = Flask(__name__)
api = Api(app)
db = DBConnection()

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

class UrlShortnerAPI(Resource):
    def get(self, short_url):
        user_agent_string = request.headers.get('User-Agent')
        user_ip = get_ip()
        user_agent = parse(user_agent_string)
        browser=user_agent.browser.family
        browser_version=user_agent.browser.version_string
        operating_system=user_agent.os.family
        device_type = determine_device_type(user_agent_string)
        location_info = get_user_agent_location(user_ip)
        city = location_info.get('city', '')
        region = location_info.get('region', '')
        country = location_info.get('country', '')
        location = location_info.get('location', '')
        referrer = request.referrer
        url_shortener_id_query = "SELECT id FROM `url_shortener` WHERE short_url = :short_url"
        url_shortener_id_params = {'short_url': short_url}
        url_shortener_id_result = db.fetch_one(url_shortener_id_query, url_shortener_id_params)

        if url_shortener_id_result:
            url_shortener_id = url_shortener_id_result[0]
            print("urlid",url_shortener_id)
            query = "INSERT INTO url_shortener_tracker (id, ip_address, device_type, operating_system, browser, version, city, region, country, location, referrer, url_shortener_id ) VALUES (:id, :ip_address, :device_type, :operating_system, :browser, :version, :city, :region, :country, :location, :referrer, :url_shortener_id)"
            params = {
                'id': str(uuid.uuid4()),
                'ip_address': user_ip,
                'device_type': device_type,
                'operating_system': operating_system,
                'browser': browser,
                'version': browser_version,
                'city': city,
                'region': region,
                'country': country,
                'location': location,
                'referrer': referrer,
                'url_shortener_id': url_shortener_id,
            }
            db.execute(query, params)


        query = "SELECT long_url, count FROM `url_shortener` where short_url = :short_url; "
        params = {'short_url': short_url}
        print(params)
        url = db.fetch_one(query, params)
        print("url",url)
        if url:
            long_url, count = url
            count += 1
            print(count)
            update_query = "UPDATE `url_shortener` SET count = :count WHERE short_url = :short_url"
            update_params = {'count': count, 'short_url': short_url}
            db.execute(update_query, update_params)
            return redirect(long_url)
        
        return {
            "hasError": True,
            "statusCode": 400,
            "message": "Url Not Found",
            "response": {}
        }


def determine_device_type(user_agent_string):
    if "Mobile" in user_agent_string:
        return "Mobile"
    elif "Tablet" in user_agent_string:
        return "Tablet"
    elif "Android" in user_agent_string:
        return "Mobile"  
    elif "iOS" in user_agent_string:
        return "Mobile"  
    else:
        return "PC"  


def get_user_agent_location(ip_address):
        try:
            response = requests.get(f'https://ipinfo.io/{ip_address}/json')
            data = response.json()
            location_info = {
                'ip': data.get('ip', ''),
                'city': data.get('city', ''),
                'region': data.get('region', ''),
                'country': data.get('country', ''),
                'location': data.get('loc', '')
            }
            return location_info
        except Exception as e:
            print(f"Error retrieving location info: {str(e)}")
            return {}
        
api.add_resource(UrlShortnerAPI, '/r/<string:short_url>/')

