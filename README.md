# mover
Some geometrical form with various movement types based in Kivy

This is a simple experiment I wrote a long time ago to understand how to make a Kivy app for Android and explore animations. I don't pretend to continue with it. Feel free to use it as you like.

![alt text](https://github.com/Aledosim/Mover/blob/main/image.jpg?raw=true)

The base code is a main App class from Kivy which creates a RelativeLayout (named Mover) and defines the movement to be executed. The Mover instance animates an figure (in this case an ellipse defined as Mass in mover.kv) accordingly with the specified movement and prints out the trace. The trace class is called Rastro, it is responsible to create copies of the Mass and change their opacities over time. The movements are defined in terms of accelerations of the "mass".
In this repository I provide the apk and the buildozer's spec file as well.
