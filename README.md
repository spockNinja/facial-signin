facial-signin
===============

A basic web app that demonstrates using facial recognition as an authentication method.

This is a project for CSC 545 at Missouri State University.


## Roadmap
* [ ] Once a user is logged in, they should be able to add a photo of themselves using a webcam.
  * [ ] Need to hook up an S3 bucket to store photos.
  * [ ] Naming convention: `[user.id]_base.ext`
  * [ ] MediaDevices.getUserMedia() in the JS to get webcam instance and photo.
* [ ] Analyze stored photo.
  * [ ] Apply filters, find recognizable features.
  * [ ] Store the analysis in a standardized JSON blob on the User.
  * [ ] Possibly store filtered intermediate photos for comparison.
* [ ] Once a user has uploaded a photo, require a match for logging in again.
  * [ ] Sucessful username/password login should check for base analysis.
  * [ ] Take a new photo, and compare it's analysis to the stored analysis.
