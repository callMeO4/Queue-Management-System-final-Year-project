AI-BASED DYNAMIC QUEUE MANAGEMENT AND OPTIMIZATION SYSTEM FOR
A BANKING ENVIRONMENT
Project Proposal
Student Name: Shammah Musukwa
Student Number: 202305900
Programme: Bachelor of Science in Computer Science
Institution: Mulungushi University
Department: [Department Name]
Supervisor: Dr. Kaluba Z.
Date of Submission: XX November 2026
⸻
ABSTRACT
Long waiting times and inefficient queue management are common challenges in service
environments such as banks. Traditional queue management approaches may provide
customers with limited information about their expected waiting times and may not distribute
workloads efficiently among available service personnel.
This project proposes the development of an AI-Based Dynamic Queue Management and
Optimization System for a banking environment. The proposed system will allow customers
to register for banking services digitally through a web interface or QR code and receive a
queue ticket. A supervised machine learning model will predict customer waiting times using
relevant queue information, including queue length, service category, service duration and
time of day.
The system will use these predictions to allocate customers to eligible tellers based on the
lowest predicted waiting time. Customers will be able to view their assigned teller, queue
position and estimated waiting time. Tellers will manage their assigned queues, while
administrators will monitor queue operations and manage system information.
The initial machine learning approach will use Linear Regression to predict waiting times. The
system will be developed using Python, Django, PostgreSQL, HTML, CSS and JavaScript,
with Scikit-learn for machine learning implementation. Its performance will be evaluated
using Mean Absolute Error (MAE) for prediction accuracy and queue-related performance
measures.
The expected outcome is a functional web-based prototype that improves queue visibility,
provides estimated waiting times and supports more efficient teller allocation.
Keywords: Queue Management, Machine Learning, Waiting Time Prediction, Linear
Regression, Dynamic Allocation, Banking System.
⸻
CHAPTER ONE: INTRODUCTION
1.1 Background of the Study
Queues are an important part of service delivery in environments where customers require
assistance from a limited number of service personnel. Banks, in particular, handle different
customer requests such as deposits, withdrawals, money transfers, account enquiries and
loan enquiries.
Traditional queue management approaches often rely on physical lines or ticket-based
systems. Although these approaches help organize customers, they may not provide
accurate information about how long customers are expected to wait. Customers may also
experience uncertainty when several service points are available but workloads are unevenly
distributed.
Advances in Artificial Intelligence (AI) and Machine Learning (ML) provide opportunities to
improve queue management by analysing historical and real-time information. Machine
learning models can identify patterns in service data and use them to estimate future waiting
times.
This project proposes an AI-Based Dynamic Queue Management and Optimization System
designed for a banking environment. The system will combine digital queue registration,
machine learning-based waiting time prediction and dynamic teller allocation.
Customers will be able to register for a banking service, receive a ticket and monitor their
queue information remotely. The system will predict waiting times for eligible tellers and
allocate each new customer to the teller with the lowest predicted waiting time.
The proposed system will also maintain queue records that can be used to improve future
predictions and evaluate the effectiveness of the system.
1.2 Problem Statement
Traditional queue management approaches in banking environments can result in long
waiting times, uneven distribution of customers among tellers and limited visibility of queue
progress.
Customers may not know how long they are expected to wait or which service point is likely
to serve them sooner. Additionally, allocating customers without considering teller
availability, service requirements and current workloads may lead to inefficient use of
available service personnel.
Although ticket-based systems help organize customers, they do not necessarily provide
intelligent waiting time predictions or dynamic allocation based on current queue conditions.
There is therefore a need for a system that can predict customer waiting times using
available queue information and allocate customers to suitable tellers based on predicted
waiting times.
This project seeks to address these challenges by developing an AI-based queue
management system that provides digital registration, waiting time prediction, dynamic teller
allocation and real-time queue monitoring.
1.3 Aim of the Project
To develop an AI-based dynamic queue management and optimization system that predicts
customer waiting times and allocates customers to suitable tellers in a banking environment.
1.4 Specific Objectives
The project will seek to:
1.
Develop a digital queue registration system that allows customers to select banking
services and receive unique queue tickets.
2.
Implement a supervised machine learning model to predict customer waiting times
using historical and real-time queue information.
3.
Develop a dynamic teller allocation mechanism that assigns customers to eligible
tellers based on predicted waiting times and service requirements.
4.
Develop a customer interface that displays queue tickets, assigned tellers, queue
positions and estimated waiting times.
5.
Develop teller and administrator dashboards for managing and monitoring queue
operations.
6.
Evaluate the system’s performance using prediction accuracy and queue management
performance measures.
1.5 Research Questions
The project will be guided by the following questions:
1.
How can machine learning be used to predict customer waiting times in a banking
queue?
2.
How can customers be dynamically allocated to suitable tellers using predicted waiting
times?
3.
How can customers be provided with clear and updated information about their queue
progress?
4.
How effective is the proposed system in predicting waiting times and improving queue
management?
1.6 Significance of the Project
The proposed system is expected to benefit the following groups:
Customers: Customers will have access to digital queue registration and information about
their assigned teller, queue position and estimated waiting time. This can reduce uncertainty
while waiting for banking services.
Bank management: Administrators will have a centralized view of queue operations and
teller availability, helping them monitor workloads and service performance.
Tellers: Tellers will be able to manage their assigned customers through a dedicated
dashboard, improving visibility and organization of their workloads.
Academic contribution: The project will demonstrate the practical application of machine
learning, database management and web development in solving a real-world service
management problem.
1.7 Scope of the Project
The project will focus on developing a web-based prototype for queue management in a
banking environment.
Included in the project
●
Digital customer queue registration.
●
QR-code-based access to the registration interface.
●
Selection of banking services.
●
Automatic generation of queue tickets.
●
Teller availability and service management.
●
Machine learning-based waiting time prediction.
●
Dynamic allocation of customers to eligible tellers.
●
Customer queue position and waiting time display.
●
Teller dashboard for managing assigned customers.
●
Administrator dashboard for monitoring queue operations.
●
Queue history and performance reporting.
●
Evaluation of prediction accuracy and queue performance.
The initial banking service categories will include:
1.
Deposits.
2.
Withdrawals.
3.
Account enquiries.
4.
Money transfers.
5.
Loan enquiries.
Excluded from the project
●
Processing actual financial transactions.
●
Integration with real banking systems.
●
Biometric identification.
●
Development of a native Android or iOS application.
●
Deployment across multiple real bank branches.
●
Physical IoT hardware integration.
The project will initially operate as a web-based prototype in a controlled environment.
1.8 Limitations of the Project
The accuracy of waiting time predictions will depend on the quality and quantity of available
queue data. Limited historical data may affect the initial performance of the machine learning
model.
Access to real banking queue records may also be restricted due to privacy and security
requirements. Where real historical records are unavailable, appropriately generated sample
or simulated data will be used for initial model development and testing.
The system will be developed as an academic prototype and will not directly interact with
real banking transaction systems.
⸻
CHAPTER TWO: LITERATURE REVIEW
2.1 Introduction
This chapter discusses existing approaches to queue management, waiting time prediction
and the application of machine learning in service environments. It also identifies the gap
that the proposed system seeks to address.
2.2 Traditional Queue Management Systems
Traditional queue management systems commonly use physical queues or ticket-based
arrangements to organize customers waiting for services.
These systems provide a basic method of maintaining service order. However, they may offer
limited information about expected waiting times and may not automatically distribute
customers according to changing service conditions.
In environments where different service personnel handle different categories of requests,
customers may also experience difficulties identifying the most suitable service point.
2.3 Machine Learning in Waiting Time Prediction
Machine learning involves developing computational models that learn patterns from data
and use those patterns to make predictions or decisions.
Waiting time prediction can be treated as a supervised learning problem because historical
queue records can provide input features and known actual waiting times as target values.
Relevant input features may include:
●
Number of customers waiting ahead.
●
Service category.
●
Average service duration.
●
Current teller workload.
●
Time of day.
●
Number of active tellers.
Chocron, Cohen and Feigin (2024) investigated queueing theory and machine learning
approaches for predicting delays in service systems. Their research demonstrates that
waiting time prediction depends on the characteristics and operating conditions of the
service environment.
2.4 Linear Regression
Linear Regression is a supervised machine learning algorithm used to predict numerical
values based on relationships between input variables and a target variable.
In this project, Linear Regression will be used to estimate customer waiting times in minutes.
The model will use relevant queue information as input features and actual waiting time as
the target variable.
Linear Regression is selected as the initial algorithm because it is relatively simple to
implement and provides an interpretable starting point for a numerical prediction problem.
Its performance will be evaluated using actual queue records.
The Scikit-learn library provides an implementation of Linear Regression that can be
integrated into the proposed system.
2.5 Dynamic Queue Allocation
Dynamic queue allocation involves assigning customers to available service points according
to changing operational conditions.
For the proposed system, a customer will first select a banking service. The system will
identify tellers who are available and capable of providing that service. The machine learning
model will estimate the waiting time associated with each eligible teller.
The allocation mechanism will then assign the customer to the eligible teller with the lowest
predicted waiting time.
The system will avoid unnecessary movement between teller queues. Customers will remain
in their assigned queues unless their assigned teller becomes unavailable. In that situation,
customers who are still waiting may be reassigned to another eligible teller.
2.6 Identified Research Gap
Traditional queue systems can organize customers but may provide limited predictive
information and may not consider changing teller workloads when assigning new customers.
Research into waiting time prediction demonstrates the potential of data-driven approaches,
but prediction alone does not provide a complete queue management solution.
The proposed project seeks to combine waiting time prediction, dynamic teller allocation,
digital customer access and queue monitoring within one integrated system designed for a
banking environment.
⸻
CHAPTER THREE: METHODOLOGY
3.1 Introduction
This chapter describes the approach that will be used to analyse, design, develop and
evaluate the proposed system.
3.2 Research and Development Approach
The project will use an iterative system development approach. The system will be developed
in stages, allowing individual components to be implemented and tested before integration.
The main development stages will include:
1.
Requirements gathering and analysis.
2.
System design.
3.
Database design.
4.
System implementation.
5.
Machine learning model development.
6.
System testing and evaluation.
3.3 Requirements Gathering
The system requirements will be identified by examining common queue management
activities in a banking environment.
The analysis will focus on the activities of customers, tellers and administrators.
The proposed system will have three main actors:
Customer
●
Register for a queue.
●
Select a banking service.
●
Receive a queue ticket.
●
View assigned teller and queue position.
●
View estimated waiting time.
●
Receive queue updates.
Teller
●
Log into the system.
●
View assigned customers.
●
Call the next customer.
●
Start customer service.
●
Complete customer service.
●
Update availability status.
Administrator
●
Manage teller accounts.
●
Manage banking service categories.
●
Monitor queues.
●
View system statistics and reports.
3.4 System Design
The system will follow a web-based client-server architecture.
The customer interface, teller dashboard and administrator dashboard will communicate
with a Django backend. The backend will manage queue operations, database interactions,
waiting time prediction and customer allocation.
The machine learning component will receive relevant queue information and generate
waiting time predictions. The queue optimization component will use those predictions to
determine the most suitable teller for each new customer.
The PostgreSQL database will store customer records, teller information, service categories,
queue tickets, assignments, predictions and notifications.
3.5 Proposed System Workflow
The system will operate through the following process:
1.
A customer accesses the system through a website or QR code.
2.
The customer selects the required banking service.
3.
The system generates a unique queue ticket.
4.
The system identifies available tellers who can handle the selected service.
5.
The machine learning model predicts the waiting time associated with each eligible
teller.
6.
The allocation mechanism selects the eligible teller with the lowest predicted waiting
time.
7.
The customer is assigned to that teller’s virtual queue.
8.
The customer can view their assigned teller, queue position and estimated waiting
time.
9.
10.
The teller calls the customer and updates the service status.
When service is completed, the system records the relevant timestamps for future
analysis and model evaluation.
If an assigned teller becomes unavailable, customers who are still waiting may be reassigned
to other eligible tellers. Their assignment history will be retained and their queue information
updated.
3.6 Machine Learning Development
3.6.1 Learning Approach
The project will use supervised machine learning because the model will be trained using
examples containing input features and known actual waiting times.
3.6.2 Selected Algorithm
The initial algorithm will be Linear Regression.
3.6.3 Input Features
Potential model features will include:
●
Queue length ahead of the customer.
●
Banking service category.
●
Average service duration for the selected service.
●
Current teller workload.
●
Time of day.
●
Number of customers currently waiting.
●
Teller availability and current service state.
The final feature set will depend on the data collected and the results of preliminary testing.
3.6.4 Target Variable
The target variable will be the actual waiting time, measured in minutes.
Actual waiting time will be calculated as:
Actual Waiting Time = Service Start Time − Registration Time.
3.6.5 Data Collection and Preparation
The system will record queue events, including registration time, service start time and
completion time.
Where access to real historical banking records is unavailable, sample or simulated queue
records will be created to support initial development and testing. The prototype will also
generate its own records during operation.
Data will be cleaned and prepared before model training. Relevant categorical variables, such
as service category, will be converted into a suitable numerical representation.
The dataset will be divided into training and testing sets to evaluate the model using data
that was not used during training.
3.6.6 Model Evaluation
The model will be evaluated using Mean Absolute Error (MAE).
MAE measures the average absolute difference between predicted waiting times and actual
waiting times.
MAE = (1/n) × Ʃ |Actual Waiting Time − Predicted Waiting Time|
A lower MAE indicates that the model’s predictions are, on average, closer to actual waiting
times.
3.7 Dynamic Allocation Mechanism
The allocation mechanism will operate after a customer selects a service.
First, the system will identify tellers who:
●
Are available to receive a new customer.
●
Are configured to provide the requested service.
The prediction model will estimate the waiting time for each eligible teller. The system will
then select the teller with the lowest predicted waiting time.
The system will maintain individual teller queues rather than one central customer queue.
This allows customers to know which teller they have been assigned to.
To prevent unnecessary queue movement, customers will not be reassigned simply because
another teller becomes available or has a shorter predicted waiting time. Reassignment will
only occur when their assigned teller becomes unavailable, and only customers who are still
waiting will be considered.
3.8 Database Design
The system will use a relational database implemented in PostgreSQL.
The initial database will consist of the following entities:
1.
User: Stores login credentials and system roles.
2.
Customer: Stores customer information.
3.
Teller: Stores teller details and availability status.
4.
Service: Stores available banking service categories.
5.
Teller
_
Service: Connects tellers to the services they can provide.
6.
Queue_
Ticket: Stores customer queue registrations and service timestamps.
7.
Queue_Assignment: Stores teller assignments and reassignment history.
8.
Wait
_
Prediction: Stores waiting time predictions generated by the machine learning
model.
9.
Notification: Stores customer notification records.
The database will use primary keys and foreign keys to maintain relationships and referential
integrity.
The Teller
_Service entity will resolve the many-to-many relationship between tellers and
banking services. Queue_Assignment will maintain assignment history rather than
overwriting previous teller assignments.
Queue positions will be calculated dynamically rather than stored as permanent ticket
values.
3.9 System Implementation
The proposed technologies are:
Component Technology
Programming language Python
Backend framework Django
Frontend HTML, CSS, JavaScript
Database PostgreSQL
Machine learning Scikit-learn
Data processing Pandas
Development environment Visual Studio Code
The system will be implemented as a web application. Django will handle application logic,
authentication and database operations, while the frontend technologies will provide the
interfaces for customers, tellers and administrators.
Python libraries will be used to prepare data, train the model and generate waiting time
predictions.
3.10 System Testing and Evaluation
The proposed system will undergo the following testing:
Functional testing: To determine whether registration, ticket generation, teller allocation,
queue updates and service management operate as expected.
Integration testing: To verify communication between the frontend, backend, database and
machine learning component.
Prediction testing: To compare predicted waiting times with actual waiting times using MAE.
Queue allocation testing: To determine whether customers are assigned only to eligible
tellers and whether the system selects the teller with the lowest predicted waiting time.
Usability testing: To assess whether customers, tellers and administrators can use their
respective interfaces effectively.
Queue performance may also be assessed by comparing average waiting times and workload
distribution under the proposed allocation mechanism against a defined baseline allocation
method.
⸻
CHAPTER FOUR: EXPECTED RESULTS
The project is expected to produce a functional web-based queue management prototype
with the following capabilities:
1.
2.
3.
4.
5.
Customers will be able to register for banking services digitally.
The system will generate unique queue tickets.
A machine learning model will estimate customer waiting times.
Customers will be assigned to eligible tellers using predicted waiting times.
Customers will be able to view their assigned teller, queue position and estimated
waiting time.
6.
7.
Tellers will be able to manage their assigned customers.
Administrators will be able to monitor queue operations and manage system
7.
information.
8.
The system will maintain historical queue records that can support model evaluation
and future improvement.
The project is expected to demonstrate how machine learning can be integrated into a queue
management application to support better waiting time information and teller allocation.
CHAPTER FIVE: PROJECT WORK PLAN
The project will be completed through the following stages. The dates will be adjusted
according to the university’s project schedule.
Activity Planned period
Proposal preparation and approval November 2026
Requirements analysis November–December 2026
System and database design December 2026
Database and backend development January 2027
Customer, teller and admin interfaces January–February 2027
Data preparation and ML model
development
February 2027
Dynamic allocation implementation February–March 2027
System integration and testing March 2027
Evaluation and documentation March–April 2027
Final presentation and submission According to university schedule
⸻
REFERENCES
Chocron, E., Cohen, I., & Feigin, P. (2024). Delay prediction for managing multiclass service
systems: An investigation of queueing theory and machine learning approaches. IEEE
Transactions on Engineering Management, 71, 4469–4479. https://doi.org/10.1109/
TEM.2022.3222094
Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). Scikit-learn: Machine learning in
Python. Journal of Machine Learning Research, 12, 2825–2830. https://jmlr.org/papers/v12/
pedregosa11a.html
Scikit-learn Developers. (n.d.). Linear regression. Scikit-learn documentation. https://scikit-
learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
Scikit-learn Developers. (n.d.). Mean absolute error. Scikit-learn documentation. https://
scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_
absolute
error.html
_
Django Software Foundation. (n.d.). Django documentation. https://docs.djangoproject.com/
PostgreSQL Global Development Group. (n.d.). PostgreSQL documentation. https://
