
## On using cluster for image processing
1. Check the input module for creating an image set
2. What is my worst case scenario? Would I have no cells? --- Not really:) And it can also be prevented by setting the lower limit, 25 - 250 pixel seems to work. 
3. Check the CreateBatchFile module. 
    1. What are the problems with relative pathnames? 
    2. Is export to database necessary? 
4. Use LoadData to import a csv file for creating a batch file. 
5. Run locally to create the batch file for cluster run.
6. **Is there a way to write a batch script to create series folders to hold the output image?** -- This can be further elucidated by reading the INPUT module doc. 

## On benchmarking the image segmentation performance. 

1. Use cell profiler to segment the cells - simple:) 
2. Custom script to segment cells out. 
3. Fit the data to hand-drawn cell boundaries (use Raj Lab tool?)
    1. StarSearch Definitely does not provide the stuff. 
    2. Use Raj Lab image tool for this -- Maybe use Ellie's code:) 
4. Compare the relative region size
