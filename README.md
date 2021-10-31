# AadhaarShala 
### Mobile App to quickly update your Aadhaar address
A lot of times, when people shift from one place to another, they need to provide a new address proofs to avail various public/private services. Getting this new address proof becomes a very tedious and time consuming task. With Aadhaar, this address update is simplified with the concept of an introducer, an Aadhaar Card holder living near your new address, who can authenticate for your new address. To make the process even simpler, we have digitised the process, using a secure way for introducer to authenticate the new address for any person.

AadhaarShala is a simple app, which uses the UIDAI APIs to authenticate the applicant and the introducer, and helps the applicant update his/her address with a simple OTP based authentication with the help of an introducer.

### Setup
##### Server Setup

### Approach
[Image for API flow]

### Security Considerations
- GPS coordinates will be used, to get approximate location of the applicant, and converted to textual address using Google Reverse Geolocation API
- Applicant requests will be deleted within 1 day, if not verified by the introducer
- Verification data will be deleted from the servers (except logs), after 1 week of successful verification to protect the users from server breaches
- Security code matching between applicant and introducer, to avoid mis-verification in case of multiple requests
- No extra personal information is stored on the server or shared with the users
- All APIs will be implemented using HTTPS protocol for encrypted communication

### Improvements
- We will use GPS coordinates of the applicant, and map it with the local address using Google's Reverse Geolocation API.
- We can expose the server APIs, for 3rd party integrations, so that they can be implemented and offered by private parties, as a service to their customers
