This is the app to solve the techical challenge task from RavenPack.
Running instructions:
   1. Clone the repo.
   2. Execute docker build -t raven-pack .
   3. Execute docker run raven-pack
 
Outcome: Application returns the stories count and errors found during file processing.
The following assumptions are made:
1. The records are not coming archived. So, extraction from rar was out of scope.
2. The file provided has fixed length, however the system is logically designed to process the records coming indefinitely from some stream. So I don't use an object to contain all the stories - in one unlucky day that will lead to out of memory. That's why I use only counter for the records but not the list of stories to count.
3. The regex pattern RP_ENTITY_ID was designed as "[A-Z|0-9]{6}". Maybe not too strict - but I couldn't find better for RP_ENTITY_ID":"KOXQBB" and RP_ENTITY_ID":"660345" as an examples.
4. All the story is coming in one time. It's unacceptable that story starts interrupting another story.
5. Checked on Windows 10. I don't have any Linux to check if instructions provided are 100% working on Linux.  
6. The following possible errors are validated (however file provided does not contain any of them so you don't see any errors in the log):
   1. The 1-st record index should be 1.
   2. Document count for all the records relates to the same story should be the same.
   3. The records for the same object should come sequentially. So, the 1-st record index should be 1, next 2 and so on.
   4. Records count should be exactly the same as the DOCUMENT_RECORD_COUNT.
What could be enhanced here:
   a). Add common channel to log the errors;
   b). Add connectors (interfaces) to make switch to another sources (for example, streams or queues) more smooth.
   ... etc
   The reason why it wasn't done - that will create unnecessary complication of code not related to the test task scope.
