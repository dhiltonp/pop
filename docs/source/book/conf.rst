=============================
Plugin Oriented Configuration
=============================

Applications need to be able to be configured. This presents a number
of unique challenges to Plugin Oriented Programming. For the concepts
around app merging to work, the loading up of configuration data at
the startup of an application must be taken into full account. The
process of loading up that data must also be pluggable.

Addressing these needs creates a difficult point of intersection.
As these points get evaluated it becomes necessary to
