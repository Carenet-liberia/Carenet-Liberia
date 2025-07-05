
import json
from main import app, db, User, HealthFacility
from werkzeug.security import generate_password_hash

# Comprehensive Health Professionals Data for Liberia
HEALTH_PROFESSIONALS = [
    # Montserrado County
    {"name": "Sarah Johnson", "profession": "Doctor", "specialization": "General Medicine", "facility": "JFK Medical Center", "county": "Montserrado", "district": "Greater Monrovia", "phone": "231-77-123-456", "email": "s.johnson@jfkmc.lr", "license": "MD-LIB-2019-001"},
    {"name": "Marcus Williams", "profession": "Doctor", "specialization": "Pediatrics", "facility": "ELWA Hospital", "county": "Montserrado", "district": "Paynesville", "phone": "231-88-234-567", "email": "m.williams@elwa.lr", "license": "MD-LIB-2020-045"},
    {"name": "Grace Tarr", "profession": "Nurse", "specialization": "Maternal Health", "facility": "Redemption Hospital", "county": "Montserrado", "district": "New Kru Town", "phone": "231-77-345-678", "email": "g.tarr@redemption.lr", "license": "RN-LIB-2018-089"},
    {"name": "Emmanuel Kollie", "profession": "Doctor", "specialization": "Surgery", "facility": "John F. Kennedy Medical Center", "county": "Montserrado", "district": "Sinkor", "phone": "231-88-456-789", "email": "e.kollie@jfkmc.lr", "license": "MD-LIB-2017-023"},
    {"name": "Mary Pewee", "profession": "Midwife", "specialization": "Obstetrics", "facility": "C.H. Rennie Hospital", "county": "Montserrado", "district": "Kakata", "phone": "231-77-567-890", "email": "m.pewee@rennie.lr", "license": "MW-LIB-2019-034"},
    
    # Bong County
    {"name": "Joseph Wreh", "profession": "Doctor", "specialization": "Internal Medicine", "facility": "Phebe Hospital", "county": "Bong", "district": "Suakoko", "phone": "231-88-678-901", "email": "j.wreh@phebe.lr", "license": "MD-LIB-2018-067"},
    {"name": "Rebecca Kpannah", "profession": "Nurse", "specialization": "Critical Care", "facility": "Phebe Hospital", "county": "Bong", "district": "Suakoko", "phone": "231-77-789-012", "email": "r.kpannah@phebe.lr", "license": "RN-LIB-2020-112"},
    {"name": "Daniel Tarnue", "profession": "Lab Technician", "specialization": "Medical Laboratory", "facility": "Bong County Hospital", "county": "Bong", "district": "Gbarnga", "phone": "231-88-890-123", "email": "d.tarnue@bong.lr", "license": "MLT-LIB-2019-056"},
    
    # Nimba County
    {"name": "Agnes Flomo", "profession": "Doctor", "specialization": "Family Medicine", "facility": "Ganta United Methodist Hospital", "county": "Nimba", "district": "Ganta", "phone": "231-77-901-234", "email": "a.flomo@ganta.lr", "license": "MD-LIB-2019-089"},
    {"name": "Patrick Sayeh", "profession": "Nurse", "specialization": "Emergency Care", "facility": "Ganta United Methodist Hospital", "county": "Nimba", "district": "Ganta", "phone": "231-88-012-345", "email": "p.sayeh@ganta.lr", "license": "RN-LIB-2018-076"},
    {"name": "Comfort Zulu", "profession": "Midwife", "specialization": "Maternal Care", "facility": "Saclepea Health Center", "county": "Nimba", "district": "Saclepea", "phone": "231-77-123-456", "email": "c.zulu@saclepea.lr", "license": "MW-LIB-2020-023"},
    
    # Grand Bassa County
    {"name": "Thomas Kpadeh", "profession": "Doctor", "specialization": "General Surgery", "facility": "C.B. Dunbar Hospital", "county": "Grand Bassa", "district": "Buchanan", "phone": "231-88-234-567", "email": "t.kpadeh@dunbar.lr", "license": "MD-LIB-2017-134"},
    {"name": "Martha Boakai", "profession": "Nurse", "specialization": "Pediatric Care", "facility": "C.B. Dunbar Hospital", "county": "Grand Bassa", "district": "Buchanan", "phone": "231-77-345-678", "email": "m.boakai@dunbar.lr", "license": "RN-LIB-2019-098"},
    
    # Lofa County
    {"name": "Samuel Kamara", "profession": "Doctor", "specialization": "Infectious Diseases", "facility": "Tellewoyan Memorial Hospital", "county": "Lofa", "district": "Voinjama", "phone": "231-88-456-789", "email": "s.kamara@tellewoyan.lr", "license": "MD-LIB-2018-201"},
    {"name": "Fatima Koroma", "profession": "Nurse", "specialization": "Community Health", "facility": "Foya Health Center", "county": "Lofa", "district": "Foya", "phone": "231-77-567-890", "email": "f.koroma@foya.lr", "license": "RN-LIB-2020-087"},
    
    # Grand Cape Mount County
    {"name": "Robert Sheriff", "profession": "Doctor", "specialization": "General Medicine", "facility": "Bomi County Hospital", "county": "Grand Cape Mount", "district": "Robertsport", "phone": "231-88-678-901", "email": "r.sheriff@bomi.lr", "license": "MD-LIB-2019-156"},
    
    # Margibi County
    {"name": "Elizabeth Tubman", "profession": "Doctor", "specialization": "Obstetrics & Gynecology", "facility": "C.H. Rennie Hospital", "county": "Margibi", "district": "Kakata", "phone": "231-77-789-012", "email": "e.tubman@rennie.lr", "license": "MD-LIB-2018-078"},
    {"name": "James Duo", "profession": "Pharmacist", "specialization": "Clinical Pharmacy", "facility": "Margibi County Hospital", "county": "Margibi", "district": "Kakata", "phone": "231-88-890-123", "email": "j.duo@margibi.lr", "license": "RPh-LIB-2019-034"},
    
    # Grand Gedeh County
    {"name": "Moses Blah", "profession": "Doctor", "specialization": "Rural Medicine", "facility": "Martha Tubman Memorial Hospital", "county": "Grand Gedeh", "district": "Zwedru", "phone": "231-77-901-234", "email": "m.blah@martha.lr", "license": "MD-LIB-2020-045"},
    
    # Sinoe County
    {"name": "Victoria Johnson", "profession": "Nurse", "specialization": "Public Health", "facility": "Sinoe County Hospital", "county": "Sinoe", "district": "Greenville", "phone": "231-88-012-345", "email": "v.johnson@sinoe.lr", "license": "RN-LIB-2018-123"},
    
    # Maryland County
    {"name": "Abraham Weeks", "profession": "Doctor", "specialization": "General Medicine", "facility": "J.J. Dossen Hospital", "county": "Maryland", "district": "Harper", "phone": "231-77-123-456", "email": "a.weeks@dossen.lr", "license": "MD-LIB-2019-089"},
    
    # River Cess County
    {"name": "Hannah Mulbah", "profession": "Nurse", "specialization": "Maternal Health", "facility": "River Cess County Hospital", "county": "River Cess", "district": "Cestos City", "phone": "231-88-234-567", "email": "h.mulbah@rivercess.lr", "license": "RN-LIB-2020-045"},
    
    # Grand Kru County
    {"name": "Peter Kpaan", "profession": "Doctor", "specialization": "Family Medicine", "facility": "Grand Kru County Hospital", "county": "Grand Kru", "district": "Barclayville", "phone": "231-77-345-678", "email": "p.kpaan@grandkru.lr", "license": "MD-LIB-2018-167"},
    
    # River Gee County
    {"name": "Comfort Weah", "profession": "Midwife", "specialization": "Obstetrics", "facility": "River Gee County Hospital", "county": "River Gee", "district": "Fish Town", "phone": "231-88-456-789", "email": "c.weah@rivergee.lr", "license": "MW-LIB-2019-078"},
    
    # Gbarpolu County
    {"name": "Francis Kanneh", "profession": "Doctor", "specialization": "General Medicine", "facility": "Gbarpolu County Hospital", "county": "Gbarpolu", "district": "Bopolu", "phone": "231-77-567-890", "email": "f.kanneh@gbarpolu.lr", "license": "MD-LIB-2020-123"},
    
    # Bomi County
    {"name": "Josephine Cooper", "profession": "Nurse", "specialization": "Pediatric Care", "facility": "Bomi County Hospital", "county": "Bomi", "district": "Tubmanburg", "phone": "231-88-678-901", "email": "j.cooper@bomi.lr", "license": "RN-LIB-2019-145"}
]

# Comprehensive Health Facilities Data for All 15 Counties
HEALTH_FACILITIES = [
    # Montserrado County
    {"name": "John F. Kennedy Medical Center", "type": "Hospital", "county": "Montserrado", "district": "Sinkor", "contact": "231-77-123-456", "gps": "6.3157,-10.7975", "services": "Emergency, Surgery, ICU, Maternity, Pediatrics, Cardiology, Oncology"},
    {"name": "ELWA Hospital", "type": "Hospital", "county": "Montserrado", "district": "Paynesville", "contact": "231-88-234-567", "gps": "6.2895,-10.7466", "services": "General Medicine, Surgery, Maternity, Pediatrics, Laboratory"},
    {"name": "Redemption Hospital", "type": "Hospital", "county": "Montserrado", "district": "New Kru Town", "contact": "231-77-345-678", "gps": "6.2742,-10.7963", "services": "Emergency, General Medicine, Maternity, Laboratory, Pharmacy"},
    {"name": "Stella Maris Polytechnic Health Center", "type": "Health Center", "county": "Montserrado", "district": "Monrovia", "contact": "231-88-456-789", "gps": "6.3008,-10.7969", "services": "Outpatient Care, Vaccinations, Family Planning, Laboratory"},
    {"name": "SKD Sports Complex Clinic", "type": "Clinic", "county": "Montserrado", "district": "Paynesville", "contact": "231-77-567-890", "gps": "6.2957,-10.7635", "services": "General Medicine, Sports Medicine, Physiotherapy"},
    
    # Bong County
    {"name": "Phebe Hospital", "type": "Hospital", "county": "Bong", "district": "Suakoko", "contact": "231-88-678-901", "gps": "6.9167,-9.5833", "services": "General Medicine, Surgery, Maternity, Pediatrics, Mental Health, Laboratory"},
    {"name": "Bong County Hospital", "type": "Hospital", "county": "Bong", "district": "Gbarnga", "contact": "231-77-789-012", "gps": "6.9986,-9.4722", "services": "Emergency, General Medicine, Surgery, Maternity, Laboratory"},
    {"name": "Cuttington University Health Center", "type": "Health Center", "county": "Bong", "district": "Suakoko", "contact": "231-88-890-123", "gps": "6.9028,-9.5694", "services": "Student Health, General Medicine, Vaccinations"},
    {"name": "Salala Health Center", "type": "Health Center", "county": "Bong", "district": "Salala", "contact": "231-77-901-234", "gps": "6.8333,-9.2500", "services": "Primary Care, Maternity, Child Health, Vaccinations"},
    
    # Nimba County
    {"name": "Ganta United Methodist Hospital", "type": "Hospital", "county": "Nimba", "district": "Ganta", "contact": "231-88-012-345", "gps": "7.2333,-8.9667", "services": "General Medicine, Surgery, Maternity, Pediatrics, Laboratory, Pharmacy"},
    {"name": "Saclepea Health Center", "type": "Health Center", "county": "Nimba", "district": "Saclepea", "contact": "231-77-123-456", "gps": "7.4167,-8.7500", "services": "Primary Care, Maternity, Child Health, Vaccinations"},
    {"name": "Tappita Hospital", "type": "Hospital", "county": "Nimba", "district": "Tappita", "contact": "231-88-234-567", "gps": "6.2833,-8.8167", "services": "General Medicine, Surgery, Emergency, Laboratory"},
    {"name": "Karnplay Health Center", "type": "Health Center", "county": "Nimba", "district": "Karnplay", "contact": "231-77-345-678", "gps": "7.1333,-8.8000", "services": "Primary Care, Maternity, Vaccinations, Laboratory"},
    
    # Grand Bassa County
    {"name": "C.B. Dunbar Hospital", "type": "Hospital", "county": "Grand Bassa", "district": "Buchanan", "contact": "231-88-456-789", "gps": "5.8811,-10.0467", "services": "General Medicine, Surgery, Maternity, Emergency, Laboratory"},
    {"name": "Compound #3 Health Center", "type": "Health Center", "county": "Grand Bassa", "district": "Buchanan", "contact": "231-77-567-890", "gps": "5.8833,-10.0333", "services": "Primary Care, Child Health, Vaccinations"},
    {"name": "Owensgrove Health Center", "type": "Health Center", "county": "Grand Bassa", "district": "Owensgrove", "contact": "231-88-678-901", "gps": "6.1667,-9.7500", "services": "Primary Care, Maternity, Laboratory"},
    
    # Lofa County
    {"name": "Tellewoyan Memorial Hospital", "type": "Hospital", "county": "Lofa", "district": "Voinjama", "contact": "231-77-789-012", "gps": "8.4217,-9.7539", "services": "General Medicine, Surgery, Maternity, Emergency, Mental Health"},
    {"name": "Foya Health Center", "type": "Health Center", "county": "Lofa", "district": "Foya", "contact": "231-88-890-123", "gps": "8.3833,-10.2000", "services": "Primary Care, Maternity, Child Health, Vaccinations"},
    {"name": "Zorzor Hospital", "type": "Hospital", "county": "Lofa", "district": "Zorzor", "contact": "231-77-901-234", "gps": "8.0833,-9.4667", "services": "General Medicine, Surgery, Maternity, Laboratory"},
    
    # Grand Cape Mount County
    {"name": "Bomi County Hospital", "type": "Hospital", "county": "Grand Cape Mount", "district": "Robertsport", "contact": "231-88-012-345", "gps": "6.7500,-11.3667", "services": "General Medicine, Surgery, Maternity, Emergency"},
    {"name": "Robertsport Health Center", "type": "Health Center", "county": "Grand Cape Mount", "district": "Robertsport", "contact": "231-77-123-456", "gps": "6.7542,-11.3689", "services": "Primary Care, Maternity, Vaccinations"},
    
    # Margibi County
    {"name": "C.H. Rennie Hospital", "type": "Hospital", "county": "Margibi", "district": "Kakata", "contact": "231-88-234-567", "gps": "6.5144,-10.3489", "services": "General Medicine, Surgery, Maternity, Pediatrics, Laboratory"},
    {"name": "Margibi County Hospital", "type": "Hospital", "county": "Margibi", "district": "Kakata", "contact": "231-77-345-678", "gps": "6.5167,-10.3500", "services": "Emergency, General Medicine, Surgery, Pharmacy"},
    {"name": "Firestone Medical Center", "type": "Medical Center", "county": "Margibi", "district": "Harbel", "contact": "231-88-456-789", "gps": "6.2833,-10.3667", "services": "Occupational Health, General Medicine, Emergency, Laboratory"},
    
    # Grand Gedeh County
    {"name": "Martha Tubman Memorial Hospital", "type": "Hospital", "county": "Grand Gedeh", "district": "Zwedru", "contact": "231-77-567-890", "gps": "6.0667,-8.1333", "services": "General Medicine, Surgery, Maternity, Emergency, Laboratory"},
    {"name": "Zwedru Health Center", "type": "Health Center", "county": "Grand Gedeh", "district": "Zwedru", "contact": "231-88-678-901", "gps": "6.0700,-8.1300", "services": "Primary Care, Child Health, Vaccinations"},
    
    # Sinoe County
    {"name": "Sinoe County Hospital", "type": "Hospital", "county": "Sinoe", "district": "Greenville", "contact": "231-77-789-012", "gps": "5.0167,-9.0333", "services": "General Medicine, Surgery, Maternity, Emergency"},
    {"name": "Greenville Health Center", "type": "Health Center", "county": "Sinoe", "district": "Greenville", "contact": "231-88-890-123", "gps": "5.0200,-9.0300", "services": "Primary Care, Maternity, Vaccinations, Laboratory"},
    
    # Maryland County
    {"name": "J.J. Dossen Hospital", "type": "Hospital", "county": "Maryland", "district": "Harper", "contact": "231-77-901-234", "gps": "4.3750,-7.7167", "services": "General Medicine, Surgery, Maternity, Emergency, Laboratory"},
    {"name": "Harper Health Center", "type": "Health Center", "county": "Maryland", "district": "Harper", "contact": "231-88-012-345", "gps": "4.3783,-7.7200", "services": "Primary Care, Child Health, Vaccinations"},
    
    # River Cess County
    {"name": "River Cess County Hospital", "type": "Hospital", "county": "River Cess", "district": "Cestos City", "contact": "231-77-123-456", "gps": "5.9000,-9.6000", "services": "General Medicine, Maternity, Emergency, Laboratory"},
    {"name": "Cestos City Health Center", "type": "Health Center", "county": "River Cess", "district": "Cestos City", "contact": "231-88-234-567", "gps": "5.9033,-9.5967", "services": "Primary Care, Maternity, Vaccinations"},
    
    # Grand Kru County
    {"name": "Grand Kru County Hospital", "type": "Hospital", "county": "Grand Kru", "district": "Barclayville", "contact": "231-77-345-678", "gps": "4.6000,-8.2333", "services": "General Medicine, Surgery, Maternity, Emergency"},
    {"name": "Barclayville Health Center", "type": "Health Center", "county": "Grand Kru", "district": "Barclayville", "contact": "231-88-456-789", "gps": "4.6033,-8.2300", "services": "Primary Care, Child Health, Vaccinations"},
    
    # River Gee County
    {"name": "River Gee County Hospital", "type": "Hospital", "county": "River Gee", "district": "Fish Town", "contact": "231-77-567-890", "gps": "4.9667,-7.9333", "services": "General Medicine, Maternity, Emergency, Laboratory"},
    {"name": "Fish Town Health Center", "type": "Health Center", "county": "River Gee", "district": "Fish Town", "contact": "231-88-678-901", "gps": "4.9700,-7.9300", "services": "Primary Care, Maternity, Vaccinations"},
    
    # Gbarpolu County
    {"name": "Gbarpolu County Hospital", "type": "Hospital", "county": "Gbarpolu", "district": "Bopolu", "contact": "231-77-789-012", "gps": "7.4167,-10.8167", "services": "General Medicine, Surgery, Maternity, Emergency"},
    {"name": "Bopolu Health Center", "type": "Health Center", "county": "Gbarpolu", "district": "Bopolu", "contact": "231-88-890-123", "gps": "7.4200,-10.8133", "services": "Primary Care, Child Health, Vaccinations"},
    
    # Bomi County
    {"name": "Bomi County Hospital", "type": "Hospital", "county": "Bomi", "district": "Tubmanburg", "contact": "231-77-901-234", "gps": "6.8500,-10.8167", "services": "General Medicine, Surgery, Maternity, Emergency, Laboratory"},
    {"name": "Tubmanburg Health Center", "type": "Health Center", "county": "Bomi", "district": "Tubmanburg", "contact": "231-88-012-345", "gps": "6.8533,-10.8133", "services": "Primary Care, Maternity, Vaccinations, Laboratory"}
]

def initialize_health_professionals():
    """Initialize health professionals in the database"""
    try:
        for prof_data in HEALTH_PROFESSIONALS:
            # Check if professional already exists
            existing = User.query.filter_by(email=prof_data['email']).first()
            if not existing:
                user = User(
                    name=prof_data['name'],
                    email=prof_data['email'],
                    password_hash=generate_password_hash('password123'),  # Default password
                    user_type='professional',
                    county=prof_data['county'],
                    contact=prof_data['phone'],
                    specialty=prof_data['specialization'],
                    license_info=prof_data['license'],
                    availability='Monday-Friday 8:00 AM - 5:00 PM',
                    is_approved=True,
                    rating=4.5 + (hash(prof_data['name']) % 10) * 0.05  # Generate varied ratings
                )
                db.session.add(user)
        
        db.session.commit()
        print(f"Successfully initialized {len(HEALTH_PROFESSIONALS)} health professionals")
        
    except Exception as e:
        print(f"Error initializing health professionals: {e}")
        db.session.rollback()

def initialize_health_facilities():
    """Initialize health facilities in the database"""
    try:
        for facility_data in HEALTH_FACILITIES:
            # Check if facility already exists
            existing = HealthFacility.query.filter_by(name=facility_data['name']).first()
            if not existing:
                # Parse GPS coordinates
                lat, lon = None, None
                if facility_data.get('gps'):
                    try:
                        lat, lon = map(float, facility_data['gps'].split(','))
                    except:
                        pass
                
                facility = HealthFacility(
                    name=facility_data['name'],
                    county=facility_data['county'],
                    facility_type=facility_data['type'],
                    address=f"{facility_data['district']}, {facility_data['county']} County",
                    contact=facility_data['contact'],
                    services=facility_data['services'],
                    latitude=lat,
                    longitude=lon
                )
                db.session.add(facility)
        
        db.session.commit()
        print(f"Successfully initialized {len(HEALTH_FACILITIES)} health facilities")
        
    except Exception as e:
        print(f"Error initializing health facilities: {e}")
        db.session.rollback()

def export_to_json():
    """Export data to JSON files for backup"""
    try:
        with open('health_professionals.json', 'w') as f:
            json.dump(HEALTH_PROFESSIONALS, f, indent=2)
        
        with open('health_facilities.json', 'w') as f:
            json.dump(HEALTH_FACILITIES, f, indent=2)
        
        print("Data exported to JSON files successfully")
        
    except Exception as e:
        print(f"Error exporting to JSON: {e}")

if __name__ == '__main__':
    with app.app_context():
        initialize_health_professionals()
        initialize_health_facilities()
        export_to_json()
