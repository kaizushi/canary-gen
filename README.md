# canary-gen
A script which generates a strong canary from a template and uploads it with SSH/scp

What a Canary Is
================

A canary is a cryptographically signed message regularly updated to let people know you are okay. This script creates such a message, helps you sign it, and then uploads to to a remote server with the scp tool that comes with SSH.

One might think a canary is useless because one could be forced into uploading it in the first place. However you should be able to excercise your right to not incriminate yourself in a way that forbids this. Canaries work in **all good countries** and could save those using your service, if it becomes compromised.

There is an issue with signed messages where they can be used against you. A vague signed message that says 'I am Albert Einstein' and nothing else could be deployed by adverseries to trick people that they are you. A good canary has a good amount of referrent information. In the case of a canary, protecting a website, is to mention the address of that website.

In the case of an onion website on Tor, which I use this for, mentioning the address in the canary binds it to the cryptography behind the hidden service itself. It therefore inherits the trust of that onion address where the canary is displayed. The more references with a canary to things it involves the merrier, as long as they are secure and reliable.

This software includes some news headlines which are fetched from a JSON API provided by [NewsAPI](https://newsapi.org) as proof it was made recently and not in the past. 

I also like to include a canary the GPG fingerprints for the keys signing it. While this information is in the PGP signature itself, I make it easier to find out of user friendliness, so users can quickly find that information.

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

You need to clone this Git repository and edit the canary-gen.py script. There are settings at the top which are important for the template system. You should edit your template as you see fit. If you are finding setting up too hard I recommend you drop by my hosting business [KLOS Hosting](https://kloshost.online) and if you buy hosting I will help you setup this script for your account.

About Kaizushi
==============

Cryptography is very important for what I do and that is hosting darkweb sites. For years this canary software has been used to upload mine to my server. You can reach me at <kaizushi@infantile.us> by email if you wish to contact me. I love a good code review! I recommend if you have problems to use Github's issues tracker.
