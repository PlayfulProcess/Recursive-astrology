"""
Astrology Chart Calculator API
Calculates planetary positions, houses, and aspects for natal charts.
Uses Skyfield for high-precision astronomical calculations (JPL ephemeris).
"""

from http.server import BaseHTTPRequestHandler
import json
import math
from datetime import datetime, timezone, timedelta
import os

# Skyfield imports
from skyfield.api import Loader
from skyfield import almanac

# Try to import timezone libraries for accurate conversion
try:
    from timezonefinder import TimezoneFinder
    import pytz
    TZ_AVAILABLE = True
    tf = TimezoneFinder()
except ImportError:
    TZ_AVAILABLE = False
    tf = None

# Initialize Skyfield - load ephemeris and timescale
# Use de421.bsp (smaller, ~17MB) or de440s.bsp for higher accuracy
# Skyfield will auto-download on first use
_eph = None
_ts = None

def get_ephemeris():
    """Load or return cached ephemeris and timescale."""
    global _eph, _ts
    if _eph is None:
        try:
            # Try to use a local cache directory for Vercel
            cache_dir = '/tmp/skyfield_cache'
            os.makedirs(cache_dir, exist_ok=True)

            # Create a Loader instance with custom cache directory
            loader = Loader(cache_dir, verbose=False)

            # Check if ephemeris already exists
            eph_path = os.path.join(cache_dir, 'de421.bsp')
            if os.path.exists(eph_path):
                print(f"Loading cached ephemeris from {eph_path}")
            else:
                print(f"Downloading ephemeris to {cache_dir}")

            _eph = loader('de421.bsp')  # ~17MB, covers 1900-2050
            _ts = loader.timescale()
            print("Ephemeris loaded successfully")
        except Exception as e:
            print(f"Error loading ephemeris: {e}")
            raise Exception(f"Failed to load ephemeris: {str(e)}")
    return _eph, _ts

# Zodiac signs in order
ZODIAC_SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

# Planet names mapped to Skyfield ephemeris names
PLANET_NAMES = {
    'sun': 'sun',
    'moon': 'moon',
    'mercury': 'mercury',
    'venus': 'venus',
    'mars': 'mars',
    'jupiter': 'jupiter barycenter',
    'saturn': 'saturn barycenter',
    'uranus': 'uranus barycenter',
    'neptune': 'neptune barycenter',
    'pluto': 'pluto barycenter'
}

# Aspect definitions (angle, orb, name)
ASPECTS = [
    (0, 8, 'conjunction'),
    (60, 6, 'sextile'),
    (90, 8, 'square'),
    (120, 8, 'trine'),
    (180, 8, 'opposition'),
    (30, 2, 'semisextile'),
    (150, 2, 'quincunx')
]


def degrees_to_zodiac(degrees):
    """Convert ecliptic longitude to zodiac sign and degree."""
    degrees = degrees % 360
    sign_index = int(degrees / 30)
    sign_degree = degrees % 30
    return {
        'sign': ZODIAC_SIGNS[sign_index],
        'signIndex': sign_index,
        'degree': sign_degree,
        'totalDegrees': degrees
    }


def calculate_sidereal_time(t, longitude):
    """Calculate Local Sidereal Time in degrees."""
    # Skyfield gives us Greenwich Apparent Sidereal Time
    gast = t.gast  # in hours
    # Convert to degrees and add longitude
    lst = (gast * 15 + longitude) % 360
    return lst


def calculate_ascendant(lst, latitude):
    """Calculate the Ascendant (rising sign) from LST and latitude."""
    # Obliquity of the ecliptic
    obliquity = 23.4393
    obl_rad = math.radians(obliquity)
    lat_rad = math.radians(latitude)
    lst_rad = math.radians(lst)

    # Calculate Ascendant using standard formula
    y = -math.cos(lst_rad)
    x = math.sin(obl_rad) * math.tan(lat_rad) + math.cos(obl_rad) * math.sin(lst_rad)

    asc = math.degrees(math.atan2(y, x)) + 180
    asc = asc % 360

    return asc


def calculate_midheaven(lst):
    """Calculate the Midheaven (MC) from LST."""
    obliquity = 23.4393
    obl_rad = math.radians(obliquity)
    lst_rad = math.radians(lst)

    mc = math.degrees(math.atan2(math.sin(lst_rad), math.cos(lst_rad) * math.cos(obl_rad)))
    if mc < 0:
        mc += 360

    return mc


def calculate_houses_placidus(ascendant, midheaven, latitude):
    """Calculate Placidus house cusps (semi-arc method)."""
    houses = []
    lat_rad = math.radians(latitude)
    obliquity = 23.4393
    obl_rad = math.radians(obliquity)

    # Houses 1, 4, 7, 10 are the angles
    houses_cusps = [0] * 12
    houses_cusps[0] = ascendant  # 1st house = ASC
    houses_cusps[9] = midheaven  # 10th house = MC
    houses_cusps[6] = (ascendant + 180) % 360  # 7th house = DSC
    houses_cusps[3] = (midheaven + 180) % 360  # 4th house = IC

    # Simplified intermediate house calculation
    # Trisect MC→ASC arc (counter-clockwise): MC → house 11 → house 12 → ASC
    # fraction 2/3 from ASC toward MC = closer to MC = house 11
    # fraction 1/3 from ASC toward MC = closer to ASC = house 12
    mc_to_asc = (ascendant - midheaven + 360) % 360
    cusp_11 = ascendant - (2.0 / 3.0) * mc_to_asc
    if cusp_11 < 0:
        cusp_11 += 360
    houses_cusps[10] = cusp_11 % 360  # House 11

    cusp_12 = ascendant - (1.0 / 3.0) * mc_to_asc
    if cusp_12 < 0:
        cusp_12 += 360
    houses_cusps[11] = cusp_12 % 360  # House 12

    # Trisect ASC→IC arc (counter-clockwise): ASC → house 2 → house 3 → IC
    # fraction 1/3 from ASC toward IC = house 2
    # fraction 2/3 from ASC toward IC = house 3
    ic = (midheaven + 180) % 360
    asc_to_ic = (ic - ascendant + 360) % 360
    cusp_2 = ascendant + (1.0 / 3.0) * asc_to_ic
    houses_cusps[1] = cusp_2 % 360  # House 2

    cusp_3 = ascendant + (2.0 / 3.0) * asc_to_ic
    houses_cusps[2] = cusp_3 % 360  # House 3

    # Houses 5, 6 are opposite of 11, 12
    houses_cusps[4] = (houses_cusps[10] + 180) % 360
    houses_cusps[5] = (houses_cusps[11] + 180) % 360

    # Houses 8, 9 are opposite of 2, 3
    houses_cusps[7] = (houses_cusps[1] + 180) % 360
    houses_cusps[8] = (houses_cusps[2] + 180) % 360

    for i in range(12):
        houses.append({
            'house': i + 1,
            'cusp': round(houses_cusps[i], 4),
            'sign': degrees_to_zodiac(houses_cusps[i])
        })

    return houses


def calculate_houses(ascendant, midheaven, latitude, house_system='placidus'):
    """Calculate house cusps based on the house system."""
    houses = []

    if house_system == 'whole-sign':
        asc_sign = int(ascendant / 30) * 30
        for i in range(12):
            houses.append({
                'house': i + 1,
                'cusp': (asc_sign + i * 30) % 360,
                'sign': degrees_to_zodiac((asc_sign + i * 30) % 360)
            })
    elif house_system == 'equal-house':
        for i in range(12):
            cusp = (ascendant + i * 30) % 360
            houses.append({
                'house': i + 1,
                'cusp': cusp,
                'sign': degrees_to_zodiac(cusp)
            })
    elif house_system in ['placidus', 'koch', 'campanus', 'regiomontanus', 'topocentric']:
        houses = calculate_houses_placidus(ascendant, midheaven, latitude)
    else:
        for i in range(12):
            cusp = (ascendant + i * 30) % 360
            houses.append({
                'house': i + 1,
                'cusp': cusp,
                'sign': degrees_to_zodiac(cusp)
            })

    return houses


def get_house_for_planet(longitude, houses):
    """Determine which house a planet is in."""
    for i in range(12):
        start = houses[i]['cusp']
        end = houses[(i + 1) % 12]['cusp']

        if start < end:
            if start <= longitude < end:
                return i + 1
        else:
            if longitude >= start or longitude < end:
                return i + 1
    return 1


def calculate_aspects(planets):
    """Calculate aspects between planets."""
    aspects = []
    planet_keys = list(planets.keys())

    for i, p1_key in enumerate(planet_keys):
        for p2_key in planet_keys[i+1:]:
            p1_lon = planets[p1_key]['longitude']
            p2_lon = planets[p2_key]['longitude']

            diff = abs(p1_lon - p2_lon)
            if diff > 180:
                diff = 360 - diff

            for aspect_angle, orb, aspect_name in ASPECTS:
                if abs(diff - aspect_angle) <= orb:
                    aspects.append({
                        'planet1': p1_key,
                        'planet2': p2_key,
                        'aspect': aspect_name,
                        'angle': aspect_angle,
                        'orb': round(abs(diff - aspect_angle), 2),
                        'exactDegrees': round(diff, 2)
                    })
                    break

    return aspects


def local_to_utc(year, month, day, hour, minute, latitude, longitude):
    """Convert local time to UTC based on coordinates."""
    local_dt = datetime(year, month, day, hour, minute, 0)

    if TZ_AVAILABLE and tf:
        try:
            tz_name = tf.timezone_at(lat=latitude, lng=longitude)
            if tz_name:
                local_tz = pytz.timezone(tz_name)
                local_dt = local_tz.localize(local_dt)
                utc_dt = local_dt.astimezone(pytz.UTC)
                return utc_dt.replace(tzinfo=None)  # Return naive UTC datetime
        except Exception as e:
            print(f"Timezone conversion error: {e}")

    # Fallback: estimate timezone from longitude
    tz_offset_hours = round(longitude / 15)
    utc_dt = local_dt - timedelta(hours=tz_offset_hours)
    return utc_dt


def calculate_lunar_nodes(t, eph, zodiac='tropical'):
    """Calculate True Lunar Nodes using Skyfield."""
    # Get positions
    earth = eph['earth']
    moon = eph['moon']
    sun = eph['sun']

    # For true node calculation, we use the Moon's orbital elements
    # Skyfield doesn't directly give us the node, so we calculate it

    # Get Julian date for calculations
    jd = t.tt  # Terrestrial Time Julian Date
    T = (jd - 2451545.0) / 36525.0  # Centuries since J2000.0

    # Mean longitude of ascending node (degrees) - high precision formula
    mean_node = (
        125.0445479
        - 1934.1362891 * T
        + 0.0020754 * T * T
        + T * T * T / 467441.0
        - T * T * T * T / 60616000.0
    )
    mean_node = mean_node % 360

    # True node corrections (main periodic terms)
    D = 297.8501921 + 445267.1114034 * T - 0.0018819 * T * T + T * T * T / 545868.0
    M = 357.5291092 + 35999.0502909 * T - 0.0001536 * T * T + T * T * T / 24490000.0
    Mp = 134.9633964 + 477198.8675055 * T + 0.0087414 * T * T + T * T * T / 69699.0
    F = 93.2720950 + 483202.0175233 * T - 0.0036539 * T * T - T * T * T / 3526000.0

    D_rad = math.radians(D % 360)
    M_rad = math.radians(M % 360)
    Mp_rad = math.radians(Mp % 360)
    F_rad = math.radians(F % 360)

    # True node correction (Meeus, Astronomical Algorithms)
    correction = (
        -1.4979 * math.sin(2 * (D_rad - F_rad))
        - 0.1500 * math.sin(M_rad)
        - 0.1226 * math.sin(2 * D_rad)
        + 0.1176 * math.sin(2 * F_rad)
        - 0.0801 * math.sin(2 * (Mp_rad - F_rad))
    )

    north_node_lon = (mean_node + correction) % 360

    # Apply ayanamsa for sidereal
    if zodiac == 'sidereal':
        ayanamsa = 24.0
        north_node_lon = (north_node_lon - ayanamsa) % 360

    south_node_lon = (north_node_lon + 180) % 360

    return north_node_lon, south_node_lon


def calculate_chart(year, month, day, hour, minute, latitude, longitude, house_system='equal-house', zodiac='tropical'):
    """
    Calculate a complete natal chart using Skyfield (JPL ephemeris).

    Args:
        year, month, day: Birth date
        hour, minute: Birth time (local time)
        latitude, longitude: Birth location coordinates
        house_system: 'equal-house', 'whole-sign', 'placidus', etc.
        zodiac: 'tropical' or 'sidereal'

    Returns:
        Dictionary with planets, houses, aspects, and angles
    """
    # Get ephemeris and timescale
    eph, ts = get_ephemeris()

    # Convert local time to UTC
    utc_dt = local_to_utc(year, month, day, hour, minute, latitude, longitude)

    # Create Skyfield time object
    t = ts.utc(utc_dt.year, utc_dt.month, utc_dt.day,
               utc_dt.hour, utc_dt.minute, utc_dt.second)

    # Get Earth for geocentric observations
    earth = eph['earth']

    # Calculate planetary positions
    planets_data = {}

    for name, eph_name in PLANET_NAMES.items():
        try:
            planet = eph[eph_name]

            # Calculate apparent position from Earth
            astrometric = earth.at(t).observe(planet)
            apparent = astrometric.apparent()

            # Get ecliptic coordinates
            lat, lon, distance = apparent.ecliptic_latlon()
            longitude_deg = lon.degrees
            latitude_deg = lat.degrees

            # Apply ayanamsa for sidereal zodiac (Lahiri)
            if zodiac == 'sidereal':
                ayanamsa = 24.0
                longitude_deg = (longitude_deg - ayanamsa) % 360

            zodiac_pos = degrees_to_zodiac(longitude_deg)

            planets_data[name] = {
                'name': name.capitalize(),
                'longitude': round(longitude_deg, 4),
                'latitude': round(latitude_deg, 4),
                'sign': zodiac_pos['sign'],
                'signIndex': zodiac_pos['signIndex'],
                'degree': round(zodiac_pos['degree'], 2),
                'isRetrograde': False  # Will calculate below
            }
        except Exception as e:
            print(f"Error calculating {name}: {e}")

    # Calculate retrograde status for planets (compare with position 1 day later)
    t_next = ts.utc(utc_dt.year, utc_dt.month, utc_dt.day + 1,
                    utc_dt.hour, utc_dt.minute, utc_dt.second)

    for name, eph_name in PLANET_NAMES.items():
        if name in ['sun', 'moon']:
            continue  # Sun and Moon don't go retrograde
        try:
            planet = eph[eph_name]
            pos_now = earth.at(t).observe(planet).apparent().ecliptic_latlon()[1].degrees
            pos_next = earth.at(t_next).observe(planet).apparent().ecliptic_latlon()[1].degrees

            # Handle wrap-around at 0/360
            diff = pos_next - pos_now
            if diff > 180:
                diff -= 360
            elif diff < -180:
                diff += 360

            planets_data[name]['isRetrograde'] = bool(diff < 0)
        except:
            pass

    # Calculate Lunar Nodes
    north_node_lon, south_node_lon = calculate_lunar_nodes(t, eph, zodiac)

    zodiac_pos = degrees_to_zodiac(north_node_lon)
    planets_data['northnode'] = {
        'name': 'North Node',
        'longitude': round(north_node_lon, 4),
        'latitude': 0.0,
        'sign': zodiac_pos['sign'],
        'signIndex': zodiac_pos['signIndex'],
        'degree': round(zodiac_pos['degree'], 2),
        'isRetrograde': True
    }

    zodiac_pos = degrees_to_zodiac(south_node_lon)
    planets_data['southnode'] = {
        'name': 'South Node',
        'longitude': round(south_node_lon, 4),
        'latitude': 0.0,
        'sign': zodiac_pos['sign'],
        'signIndex': zodiac_pos['signIndex'],
        'degree': round(zodiac_pos['degree'], 2),
        'isRetrograde': True
    }

    # Calculate angles (Ascendant, Midheaven)
    lst = calculate_sidereal_time(t, longitude)
    ascendant = calculate_ascendant(lst, latitude)
    midheaven = calculate_midheaven(lst)

    if zodiac == 'sidereal':
        ayanamsa = 24.0
        ascendant = (ascendant - ayanamsa) % 360
        midheaven = (midheaven - ayanamsa) % 360

    # Calculate houses
    houses = calculate_houses(ascendant, midheaven, latitude, house_system)

    # Add house positions to planets
    for name in planets_data:
        planets_data[name]['house'] = get_house_for_planet(planets_data[name]['longitude'], houses)

    # Calculate aspects
    aspects = calculate_aspects(planets_data)

    return {
        'planets': planets_data,
        'houses': houses,
        'angles': {
            'ascendant': {
                'longitude': round(ascendant, 4),
                **degrees_to_zodiac(ascendant)
            },
            'midheaven': {
                'longitude': round(midheaven, 4),
                **degrees_to_zodiac(midheaven)
            },
            'descendant': {
                'longitude': round((ascendant + 180) % 360, 4),
                **degrees_to_zodiac((ascendant + 180) % 360)
            },
            'imumCoeli': {
                'longitude': round((midheaven + 180) % 360, 4),
                **degrees_to_zodiac((midheaven + 180) % 360)
            }
        },
        'aspects': aspects,
        'settings': {
            'houseSystem': house_system,
            'zodiac': zodiac,
            'ephemeris': 'Skyfield (JPL DE421)'
        }
    }


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Handle chart calculation requests."""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            # Extract parameters with validation
            try:
                year = int(data.get('year'))
                month = int(data.get('month'))
                day = int(data.get('day'))
                hour = int(data.get('hour', 12))
                minute = int(data.get('minute', 0))
                latitude = float(data.get('latitude'))
                longitude = float(data.get('longitude'))
            except (TypeError, ValueError) as e:
                raise ValueError(f"Invalid input parameters: {e}")

            house_system = data.get('houseSystem', 'placidus')
            zodiac = data.get('zodiac', 'tropical')

            # Validate ranges
            if not (1 <= month <= 12):
                raise ValueError(f"Invalid month: {month}")
            if not (1 <= day <= 31):
                raise ValueError(f"Invalid day: {day}")
            if not (0 <= hour <= 23):
                raise ValueError(f"Invalid hour: {hour}")
            if not (0 <= minute <= 59):
                raise ValueError(f"Invalid minute: {minute}")
            if not (-90 <= latitude <= 90):
                raise ValueError(f"Invalid latitude: {latitude}")
            if not (-180 <= longitude <= 180):
                raise ValueError(f"Invalid longitude: {longitude}")

            # Calculate chart
            result = calculate_chart(
                year, month, day, hour, minute,
                latitude, longitude,
                house_system, zodiac
            )

            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))

        except ValueError as e:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': str(e),
                'message': f'Invalid input: {str(e)}'
            }).encode('utf-8'))
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Chart calculation error: {error_trace}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': str(e),
                'traceback': error_trace,
                'message': f'Failed to calculate chart: {str(e)}'
            }).encode('utf-8'))

    def do_GET(self):
        """Handle GET requests (for testing and health check)."""
        try:
            # Pre-load ephemeris on GET request (useful for warming)
            eph, ts = get_ephemeris()
            ephemeris_loaded = eph is not None

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'ok',
                'ephemeris_loaded': ephemeris_loaded,
                'timezone_available': TZ_AVAILABLE,
                'message': 'Astrology Chart Calculator API (Skyfield/JPL DE421). Send POST request with birth data.',
                'example': {
                    'year': 1990,
                    'month': 6,
                    'day': 15,
                    'hour': 14,
                    'minute': 30,
                    'latitude': 40.7128,
                    'longitude': -74.0060,
                    'houseSystem': 'placidus',
                    'zodiac': 'tropical'
                }
            }).encode('utf-8'))
        except Exception as e:
            import traceback
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'error',
                'error': str(e),
                'traceback': traceback.format_exc(),
                'message': f'Failed to initialize: {str(e)}'
            }).encode('utf-8'))
