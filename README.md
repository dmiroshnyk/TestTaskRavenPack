This is the app to solve the techical challenge task from RavenPack.
Running instructions: <will be updated>
Outcome: application creates log.log file in the root folder. Please check it for the answer regarding the number of stories (and possible errors found during analysis).
The following assumptions are made:
1. The records are not coming archived. So, extraction from rar was out of scope.
2. The file provided has fixed length, however the system is logically designed to process the records coming indefinitely from some stream. So I don't use an object to contain all the stories - in one unlucky day that will lead to out of memory. That's why I use only counter for the records but not the list of stories to count.
3. The regex pattern RP_ENTITY_ID was designed as "[A-Z|0-9]{6}". Maybe not too strict - but I couldn't find better for RP_ENTITY_ID":"KOXQBB" and RP_ENTITY_ID":"660345" as an examples.
4. All the story is coming in one time. It's unacceptable that story starts interrupting another story.
5. The following possible errors are validated:
   1. The 1-st record index should be 1.
   2. Document count for all the records relates to the same story should be the same.
   3. The records for the same object should come sequentially. So, the 1-st record index should be 1, next 2 and so on.
   4. Records count should be exactly the same as the DOCUMENT_RECORD_COUNT.
What could be enhanced here:
   a). Add common channel to log the errors;
   b). Add connectors (interfaces) to make switch to another sources (for example, streams or queues) more smooth.
   ... etc
   The reason why it wasn't done - that will create unnecessary complication of code not related to the test task scope.
