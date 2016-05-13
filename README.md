facial-signin
===============

A basic web app that demonstrates using facial recognition as an authentication method.

This is a project for CSC 545 at Missouri State University.


## Roadmap
* [X] Once a user is logged in, they should be able to add a photo of themselves using a webcam.
* [X] Analyze user photo, mapping points to facial features.
* [X] Send analysis mapped to user's face back to the user for confirmation.
* [X] Once the user verifies the face mapping, save it to the user db record.
* [X] Once a user has verified a photo, require a match when they log in again.
  * [X] Match photo to user using facialInfo.py:isSamePerson.
  * [X] Use ratio of face_width combined with the variance.
* [ ] Capture eye color and add it to comparison points.
* [ ] Find a better way to account for distance from the camera.
* [ ] Tune thresholds and comparison algorithm for more accurate results.
