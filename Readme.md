# Password cracker tool

Passwords are the most common method of security. So, this project will be a tool created to try and break passwords so we can understand common pitfalls when it comes to creating passwords. You might wonder isn't it dangerous to put a password cracking toolkit on-line? Well, modern day security is based on the methods that methods are exposed we don't rely on ignorance for protection. Furthermore, anything this project will be able to do is done more efficiently by other on-line tools available for free. So, the point of this project isn't to create a revolutionary password cracker tool. But, instead to compile variety of techniques to show how passwords are cracked so that we can build tools to be better prepared. 

It is easier to think about breaking than defending because when you try to create a defense tool you don't look for tiny cracks in your security system. So, to get better at securing things you must learn about ways to break them. 

This project has 3 parts that are implemented: password cracking, extracting and using hashes, and running on-line attacks


## Part 1: Password cracking

This part of the project will be used to locally crack passwords using different types of attacks hacker common utilize: brute-force, dictionary, rules and hybrid. 

brute-force-> simple as it sounds just try everything. We can make faster by limiting the the character space to commonly used characters.

dictionary-> two main categories: custom word-list, common words
common words - Most English speaker know from 50 000 - 150 000 words. Try different combinations of them to get a better attempt at cracking password.

Custom word-list - Use a word-list as your basis and try those attack out. This can be the most common passwords or we can analyze any current passwords we have and see if certain words are more likely to be repeated and then use them. This is called spidering

Rule attacks are used to enhance other attacks by specifying how passwords are most likely to be varied.
A big sub-category are mask attacks where we swap out placeholder for commonly swaps. Like trying capitalizing different letters or swapping 1 for ! or l and a for @ and so on.

Hybrid we combine technique through careful analysis. We know most numbers come at the end of passwords. So, custom word attack and add in a brute force with just number for 6 digits. This makes password cracking more viable


Professional grade tools that do the same thing better: hashCat, john the ripper

## Part 2: Cracking hashes.

The second part of the project is to use different techniques to get and utilize hashed passwords

The first part of this getting the tables. So, we will go over common pawning techniques like cross-site -scripting , SQL injection, man-in-the browser, sniffing packets attack and so on

If we can somehow get access to the hashed version of passwords we can try to crack the password.
A super simple way of doing this is using rainbow table to crack hashes. However this only works on non-salted passwords. We will also go over ways to go over salted passwords if possible.

professional grade version tools: burp suite, wireShark, openVas, SQlMap

## Part 3: Running attacks on-line

This part of the project will try to utilize the password cracking capabilities to run attacks on-line. We will go over common barriers such as being locked out for trying to many passwords, overwhelming server with request and try to use some common techniques to overcome.
We will try to run this attack on a dummy website and try to break it.

We will also try to see if we can run attack on Wi-Fi connections

professional grade tools: hydra, 

## Part 4: Unimplemented aspects

Things not implemented by should be kept in mind when discussing password cracking.
Most passwords aren't cracked with tools but by tricking people into giving their passwords or by using simpler recovery methods.
Social engineering
Phishing
Shoulder surfing 

Defense idea - multi-factor authentication

## Part 5: language choice: Python
Why python? easier to build so good for prototyping, lot of available resources, good to demonstrate idea

cons: slower, less efficient, doesn't have low level control that languages like c have, 

## Paper

[docs](https://docs.google.com/document/d/1fB2ADr3TwQNj8fiEOXG_1yNYN64iaTsZSpFvfI_nk6Q)

## Future implementation
1. Scan website for vulnerabilities -> For now can demonstrate by using software like burp suite
2. Will allow custom character set for mask in future


### Hash mode
1. Enter hash and search for it
3. *Sniff packets for hashes*
4. *Potentially identify hashes*

### On-line mode
1. Attack Wi-Fi
2. Connect to socket


Hashes to include
SHA-1
SHA-2
NIST
MD-5
