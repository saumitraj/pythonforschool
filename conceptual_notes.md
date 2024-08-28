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

As you can see, you can have *two* states in this circuit i.e. the Bulb lights up or is "On" when the switch is pressed and it does not light up or is "Off" when the switch is pressed again!

Now let us consider two such set ups so that one case control the two bulbs independently. Therefore, we have Switch S1 controlling a Bulb which is powered by battery B1 and a Switch S2 controlling a Bulb powered by Battery B2. You will notice that now this allows us to *four* states as shown in the table!

![Two Circuits with independently controlled Bulbs with two Switches](TwoSwitches.png)

Extending this further, if we have three independent switches, we can control three bulbs giving rise to *eight* states as seen in the table!
![Three Circuits with independently controlled Bulbs with three Switches](ThreeSwitches.png)

As you can notice, each circuit can have two states but combining those circuits gives rise to  2<sup>n</sup> states where n is the number of circuits! 
Why is this important to know? This is important because this is the foundation of how computers represent and store data. In a real computer, the **circuits** are replaced by electronic components called as transistors which can be switched on and off. Millions of such transitors go into what we call micro processor chips such as the Intel/AMD processor or ARM processor as well as in memory modules.

Let's take a simple example of a *eight bit* processor. This means that the processor can deal with information coming out of at the most *eight* equivalent circuits of the type that we have seen from the bulb like examples above. How is this information represented? 

Consider this table:

| 0 | 1 | 0 | 1 | 1 | 0 | 1 | 1 |
|---|---|---|---|---|---|---|---|

This table is a representation of the "states" of those switches - 0 repersenting a OFF and 1 representing an ON. How do we interpret these states? 
- One way of interpreting this state is to simply look at these states being a binary number and convert binary to decimal using powers of two i.e. 01011011 can be written starting from units place as
  - 1x2<sup>0</sup> + 1x2<sup>1</sup> + 0x2<sup>2</sup> + 1x2<sup>3</sup> + 1x2<sup>4</sup> + 0x2<sup>5</sup> + 1x2<sup>6</sup> + 0x2<sup>7</sup>
  - = 1+2+0+8+16+0+64+0 = 91!
 
Now 91 is a number using *one* interpretation. It can also be interpreted as a character **[** if we apply the [ASCII](https://en.wikipedia.org/wiki/ASCII) "encoding" standards. Thus the electronics in computers can control and manipulate bits or switches which is represented as "information" by applying appropriate encoding standards. 
> Instructing the computer how to manipulate electronic circuits in the form of processors and memory and interpret the resulting information is precisely what is done by computer programmers!
Typical computer programmers do not operate at the level in which they think in terms of bits. The lowest level of tasks including bit manipulation are made available in simple English language like "instructions" for various types of CPUs. They are interpreted as binary values by that processor. 
