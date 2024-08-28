# Introduction

According to the [Python Software Foundation](https://www.python.org/doc/essays/blurb/?external_link=true), the organization behind Python, 
> Python is an interpreted, "object oriented", high level programming language with dynamic semantics.

Please note that as Python and its associated libraries is an extremely large subject that can be used to solve any computer science problem and takes many years to master. We shall remain focussed on concepts that are relevant in the context of data, machine learning and AI.

Now, let us unpack these terms one by one to understand what it means. However, before we do that, we need to dwell into the basics of how computers work!

# What is a computer and how does it work

We use computers everywhere - not just our laptop/desktop computers but we use them for everything from simple calculators to controlling timing on the microwave ovens, our refrigerators, our cars, sometimes even our homes, the mobile phones! Virtually everything around us use computers in some form and the fundamental question to ask is why is that so? 

The answer lies in some of these features of computers:

1. Computers can calculate very fast and with numbers of size that the human mind simply cannot deal with
2. Computers can do certin tasks repetitively  
3. Computers can also control certain devices based on these calculations 
4. Computers can generate data based on existing data using mathematical models

So what are the foundations of computer then? The answer lies in understanding a little bit of electronics. We will not dwell into a detailed exposition on electronics but just undertand it at a conceptual level to help us understand how computers work. Consider a simple electronic circuit consisting of a Battery B1, a Switch S1 and a BulbB. 

![Single Circuit with a Bulb and a Switch](SingleSwitch.png)

As you can see, you can have two states in this circuit i.e. the Bulb lights up or is "On" when the switch is pressed and it does not light up or is "Off" when the switch is pressed again!

Now let us consider two such set ups so that one case control the two bulbs independently. Therefore, we have Switch S1 controlling a Bulb which is powered by battery B1 and a Switch S2 controlling a Bulb powered by Battery B2. You will notice that now this allows us to four states as shown in the table!

![Two Circuits with independently controlled Bulbs with two Switches](TwoSwitches.png)
