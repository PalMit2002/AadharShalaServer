# AadhaarShala 
### Mobile App to quickly update your Aadhaar address
A lot of times, when people shift from one place to another, they need to provide a new address proofs to avail various public/private services. Getting this new address proof becomes a very tedious and time consuming task. With Aadhaar, this address update is simplified with the concept of an introducer, an Aadhaar Card holder living near your new address, who can authenticate for your new address. To make the process even simpler, we have digitised the process, using a secure way for introducer to authenticate the new address for any person.

AadhaarShala is a simple app, which uses the UIDAI APIs to authenticate the applicant and the introducer, and helps the applicant update his/her address with a simple OTP based authentication with the help of an introducer.

### Setup
##### Server Setup

### Approach
![Architecture Diagram - I](https://github.com/PalMit2002/AadharShalaServer/blob/main/images/im1.png?raw=true)
![Architecture Diagram - II](https://github.com/PalMit2002/AadharShalaServer/blob/main/images/im2.png?raw=true)

### Security Considerations
- GPS coordinates will be used, to get approximate location of the applicant, and converted to textual address using Google Reverse Geolocation API
- Applicant requests will be deleted within 1 day, if not verified by the introducer
- Verification data will be deleted from the servers (except logs), after 1 week of successful verification to protect the users from server breaches
- Security code matching between applicant and introducer, to avoid mis-verification in case of multiple requests
- No extra personal information is stored on the server or shared with the users
- All APIs will be implemented using HTTPS protocol for encrypted communication

### Improvements
- We will use GPS coordinates of the applicant, and map it with the local address using Google's Reverse Geolocation API.
- We can expose the server APIs, for 3rd party integrations, so that they can be implemented and offered by private parties, as a service to their customers.

## Appendix
### UIDAI API usage
We have used a number of UIDAI APIs to implement and secure our solution. Some of the APIs used are listed below:
- OTP Auth API - This API is used to authenticate the applicant and the introducer with their Aadhaar credentials. This API helps us in verifying the credibility of the users in a simple yet secure way, avoiding rogue users from scamming the system.
- eKYC API - This API is used to get the address of the introducer, which is then sent to the applicant, for minor modifications. Other non-essential details of the users are not saved anywhere in the solution.

### User Models
We are using 2 basic data models to store details related to the Applicant, and the Introducer:
**Introducer**
```
{
    "aadharnum": "9999123456789012", # Aadhaar number / VID of the introducer
    "co": "101", # 
    "house": "404", # House Number of the introducer
    "street": "04", # Street Number
    "lm": "?",
    "loc": "Locality", # Locality
    "vtc": "?",
    "subdist": "Powai", # Subdistrict
    "dist": "Powai", # District
    "state": "Maharashtra", # State
    "country": "India", # Country
    "pc": "", 
    "po": "400076", # Postal code
    "token": "05822338-55a7-416f-9e43-b00f905c943e", # Unique token (UUID4)
    "time": "2021-10-31T21:42:05.017403", # Time of registration (ISO Format)
}
```
**Applicant**
```
{
    "aadharnum": "9999123456789012", # Aadhaar number / VID of the introducer
    "mod_co": "101", # 
    "mod_house": "404", # House Number of the introducer
    "mod_street": "04", # Street Number
    "mod_lm": "?",
    "mod_loc": "Locality", # Locality
    "mod_vtc": "?",
    "mod_subdist": "Powai", # Subdistrict
    "mod_dist": "Powai", # District
    "mod_state": "Maharashtra", # State
    "mod_country": "India", # Country
    "mod_pc": "", 
    "mod_po": "400076", # Postal code
    "landlord": "101", # Landlord (introducer) object reference
    "request_code": "5839", # Request code to maintain privacy
    "is_req_active": "True", # Boolean showing if request is active
    "token": "05822338-55a7-416f-9e43-b00f905c943e", # Unique token (UUID4)
    "time": "2021-10-31T21:42:05.017403", # Time of registration (ISO Format)
}
```

### Mobile App Screenshots

### Internal APIs
