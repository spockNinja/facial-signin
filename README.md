facial-signin
===============

A basic web app that demonstrates using facial recognition as an authentication method.

This is a project for CSC 545 at Missouri State University.


## Roadmap
* [X] Once a user is logged in, they should be able to add a photo of themselves using a webcam.
* [X] Analyze user photo, mapping points to facial features.
* [ ] Send analysis mapped to user's face back to the user for confirmation.
* [ ] Once the user verifies the face mapping, save it to the user db record.
* [ ] Match photo to user using facialInfo.py:isSamePerson.
  * [ ] Use ratio of face_width combined with the variance.
* [ ] Once a user has verified a photo, require a match when they log in again.
