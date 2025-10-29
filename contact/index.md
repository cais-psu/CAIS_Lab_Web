---
title: Contact
nav:
  order: 5
  tooltip: Email, address, and location
---

# {% include icon.html icon="fa-regular fa-envelope" %}Contact

##Openings
The CAIS lab is seeking graduate and undergraduate students to join the team. Students interested in joining should be motivated and hard-working individuals who are interested in one or more of the following topics:

Control theory and applications
Dynamic systems
Industrial automation
Applied artificial intelligence
Smart manufacturing/Industry 4.0
Robotics


{%
  include button.html
  type="email"
  text="iqk5135@psu.edu"
  link="iqk5135@psu.edu"
%}

{%
  include button.html
  type="address"
  text="107 Leonhard Building"
  tooltip="Our location on Google Maps for easy navigation"
  link="https://maps.app.goo.gl/U1Mg42kpajPp4ukQA"
%}



{% include section.html %}

{% capture col1 %}

{%
  include figure.html
  image="images/photo.jpg"
  caption="Lorem ipsum"
%}

{% endcapture %}

{% capture col2 %}

{%
  include figure.html
  image="images/photo.jpg"
  caption="Lorem ipsum"
%}

{% endcapture %}

{% include cols.html col1=col1 col2=col2 %}

{% include section.html dark=true %}

{% capture col1 %}
Lorem ipsum dolor sit amet  
consectetur adipiscing elit  
sed do eiusmod tempor
{% endcapture %}

{% capture col2 %}
Lorem ipsum dolor sit amet  
consectetur adipiscing elit  
sed do eiusmod tempor
{% endcapture %}

{% capture col3 %}
Lorem ipsum dolor sit amet  
consectetur adipiscing elit  
sed do eiusmod tempor
{% endcapture %}

{% include cols.html col1=col1 col2=col2 col3=col3 %}
