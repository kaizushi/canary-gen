# canary-gen
A script which generates a strong canary from a template and uploads it with SSH/scp

What a Canary Is
================

A canary is a cryptographically signed message regularly updated to let people know you are okay. This script creates such a message, helps you sign it, and then uploads to to a remote server with the scp tool that comes with SSH.

One might think a canary is useless because one could be forced into uploading it in the first place. However you should be able to excercise your right to not incriminate yourself in a way that forbids this. Canaries work in **all good countries** and could save those using your service, if it becomes compromised.

Features
========

This script has the following features...

* Multiple GPG identities (one can sign the canary with many keys)
* Easy template system (one can change the look and feel easily)
* It fetches todays news! (this can prove the message was not signed well in the past)
* Works beautifully with picosite (another one of my hidden services)

I highly recommend using it alongside my [picosite](https://github.com/kaizushi/picosite) software which is a 'read only CMS.' Content for it is uploaded using SSH. This makes it seamless for this script to upload the canary.

You can see it in action alongside picosite over at the website for my businesses [canary page](https://kloshost.online/page.php?q=canary). I just run this script to update it and if everything works I need not do anything else.

Getting Started
===============

You need to clone this Git repository and edit the canary-gen.py script. There are settings at the top which are important for the template system. You should edit your template as you see fit. If you are finding setting up too hard I recommend you drop by my hosting business [KLOS Hosting](https://kloshost.online) and if you biy hosting I will help you setup this script with it.

About Kaizushi
==============

Cryptography is very important for what I do and that is hosting darkweb sites. For years this canary software has been used to upload mine to my server. You can reach me at <kaizushi@infantile.us> if you need to.
