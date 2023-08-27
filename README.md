# Network Users Manager

  User Management and Data Access Control System for Server Administration<br>
  In this desktop application, we efficiently manage user access and data retrieval.<br>
  Features:<br>
    • User Management: Add, remove, update, and list users effortlessly. Maintain crucial user information such as userID, username, password, firstName, lastName, and status (blocked or active).<br>
    • IP Blacklisting: Maintain a dynamic blacklist of IP addresses, preventing unauthorized access. Easily add or remove IP addresses from the blacklist to enhance security measures, similar to access lists.<br>
    • File Control: Store user-specific files in a well-organized manner. Associate users with their respective files using the files table (userID, fileName). Actual file content is securely stored in the server's designated directory.<br>
    • Administrative Actions: Administer user actions directly from the server software interface. Block/unblock users by their usernames or IP addresses. When blocked, users are prevented from accessing the server, and detailed block reasons are conveyed via textual messages.<br>
  <br>
  User Scenario:<br>
    • User Authentication: only upon successful login, users gain access to upload and download files securely from the server. a user would get files only uploaded by his/her side.<br>
    • Access Control: Users can be blocked based on their username and/or IP address. In such cases, the server promptly sends informative messages detailing the reasons for the block, enhancing transparency.<br>
<br>
  Apparatus: Python 3 | Python Modules to download: tkinter for GUI | Database with the Server (Change database info in dbConnection.py) <br>

![](1_Connecting_Peers.png)
![](2_Sending_Files_P2P.png)
![](3_Download_Received_File.png)
![](3_The_File_Downloaded_Without_Errors.png)
![](4_Choose_Directory.png)
![](4_Download_File_Already_Sent.png)
![](4_The_File_Downloaded_Without_Errors.png)
![](5_Heigh_Error_Rate_Warning.png)
