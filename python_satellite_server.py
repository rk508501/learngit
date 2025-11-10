from flask import Flask, jsonify

app = Flask(__name__)

satellites = [
    {"name": "ACE (Advanced Composition Explorer)", "description": "Studies cosmic rays and solar wind."},
    {"name": "ACRIMSAT (Active Cavity Irradiance Monitor Satellite)", "description": "Measures solar irradiance."},
    {"name": "ACS3 (Advanced Composite Solar Sail System)", "description": "Demonstrates solar sailing technology."},
    {"name": "ADEOS / Midori (Advanced Earth Observing Satellite)", "description": "Observes Earth's environment."},
    {"name": "AIM (Aeronomy of Ice in the Mesosphere)", "description": "Studies polar mesospheric clouds."},
    {"name": "AirMOSS (Airborne Microwave Observatory of Subcanopy and Subsurface)", "description": "Measures forest structure (satellite component)."},
    {"name": "Aquarius", "description": "Measures ocean surface salinity."}
    # You can extend this array by adding entries from https://www.nasa.gov/a-to-z-of-nasa-missions/
]

@app.route('/satellites', methods=['GET'])
def get_satellites():
    return jsonify(satellites), 200

def find_satellite(n):
    target = n.lower()
    for s in satellites:
        if target in s['name'].lower():
            return s
    return None

@app.route('/satellites/<n>', methods=['GET'])
def get_satellite(n):
    satellite = find_satellite(n)
    if satellite:
        return jsonify(satellite)
    return jsonify({"error": "Satellite not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
