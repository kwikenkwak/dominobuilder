Dominobuilder
=============

Blender add-on that generates lines of dominoes very fast

Installation
------------

-   Download the dominobuilder.py file from this repository.
-   Open blender and go to Edit-&gt;Preferences-&gt;Add-ons.
-   Click on install and choose the dominobuilder.py file.
-   Click the check button to enable the add-on.

Usage
-----

This add-on generates a line of dominoes based on a given curve, you can
choose which object is used as dominobrick.

### Settings

#### Set exact amount

Click this on if you want to specify the specific amount of dominoes
instead of the add-on automatically calculating the amount based on a
given spacing.

#### Spacing(visible when set exact amount is disabled)

The amount of spacing between each domino which is relative to the width
of each domino(y dimension). Tip: 4 looks good and falls well.

#### Amount(visible when set exact amount is enabled)

The amount of dominoes which are spread equally along the curve.

#### Scale

Set the scale of each domino relative to the size of the source brick.

#### Mass

Set the rigid body mass each domino has

#### Dominobrick

Set the object which will get used as the dominobricks if you want a
pretty nice standard domino with procedural shaders checkout the
standarddomino.blend file in this repository.

#### Curve

Set the curve object on which the dominoes will get spread.

#### Update dominoes

Updates the dominoes, use this when you made changes to the curve or to
the standard dominobrick.

### Why use this add-on? This is pretty easy to do in Blender without help

This addon has multiple advantages over the default blender approuch.
You can set the amount of spacing between the dominoes Most importantly
this add-on makes the objects much faster, especially setting the bricks
as rigidbody will take a lot of time if you use the copy rigidbody from
active tool in Blender which is pretty ineffiently implemented
