[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/tdy6BFPL)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=15808790&assignment_repo_type=AssignmentRepo)
# ECE1390 Semester Project: Shopkeepr

Shopkeepr 

Description: The Shopkeepr is an inventory-tracking service that identified, counts, and monitors stock for use in grocery stores. This service tracks stock on shelves to assist stores in managing stock count to ensure consumer supplies are maintained and depletions are mitigated. By taking video or still image input, the service detects objects on shelves, identifies unique items, counts items, and track data over time of the service for store and consumer data analytics. This way the store knows when stock is usually low, when it needs to be restocked, and consumers know when optimal times are to get their items with high success rates. The input would consist of a white shelf with an arrangement of cans of soup, pasta boxes, and ketchup bottles. 

Code Specifications: The code specifications for Shopkeepr are as follows: 
Inputs of a still image and up to a 30 fps stream of Takes in an a video with a frame rate of 30 frames per second 
Takes in multiple video feeds 
Output the live feed of 30 frames per second annotated with the statistics generated within the algorithm 
The video should be a live feed 

Planned Approach: I think the very first goal is to be able to identify a single item and then eventually get to separate goods. Looking at a shelf, it should be able to identify Pasta Boxes, Canned Goods, and Fruits separately. Then see if we can find a way for users to train models with their own goods. After this there will be a need to find a way to keep metrics of quantities of each good and see how to keep track if a good is taken away or placed back, etc,. Maybe multiple views will be needed. 

Timeline: 
9/27 - Github Repository & Code Claiming 
10/4 - Materials gathered (Video feed method) & Individual completion of at least 20% of goal 
10/11 - Further Progress 30-50 
10/18 - Bare Minimum Functionality V0
10/25 - Further Progress 80%
11/1 - 50-60
11/8 - V1 complete (rough model)  Everything must be attempted prior to code swap 
11/15 - Debug & Test & Improve 
11/29 - Debug & Test & Solidify Demo 
12/9 - Present
 

Metrics of Success: The early success metric will be the program's ability to accurately count and identify the items that are captured in the camera feed. Essentially, we can get an updated quantity regardless of if we add, remove, or shift items in frame. Should we finish early, an additional success metric would be to set this up at an actual grocery store shelf, or a simulated shelf that we fill with items and test the accuracy of count from our program detection. Additionally, it should be able to track both items in live video as well as hand movements. 

Pitfalls & Alternatives: If things get difficult, we could always choose to avoid video use in the project and focus primarily on frame-by-frame comparison, which would still be targeting the primary objective of the Shopkeepr, being keeping inventory and track of what is available in stock. 
One place we may expect trouble is cascaded products that are placed in line with each other. Depending on where the camera is mounted this could make identifying all objects in frame very simple or challenging, so we plan on properly setting up such that we can view all objects to some extent. Essentially, so long as we can see part of the item, we can use edge detection and tracking to keep the count updated appropriately. 

 
