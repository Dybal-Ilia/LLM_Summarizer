Here's the instruction on how to use the summarizer


1) summarizer.py file is the summarizer pipeline. You don't actually need to change anything in this file.
Just if you want to get acquainted with the provied solution, there are comment sections in the code explaining
supposedly confusing parts.


2) app.py file is the app itself. Launching this file will launch the mini-app at your localhost. The interface
is quite primitive and user-friendly:
  - You'll see the textbox called "Input Text". It's where you can paste your text manually. You can insert kinda
large texts without any prohibitions.
  - Next you'll see a section called 'Upload .txt or .pdf file'. It's where you can upload your file. Note that
the app doesn't work with .docx files so be careful and make sure that you upload an appropriate format of file.
  - The button "submit" will start the summarization process. In case no text is inserted and no file is uploaded
you'll get the erro message "Seems like an error occurred... Check whether the input is not empty". Otherwise,
if you try both to paste text manually and upload a file, the model will summarize only the text from the file.
So be careful and always make sure that you gave the model necessary text.
  - The button "Clear" just clears the "Input Text" textbox and deletes uploaded file.
  - The "Summary" textbox is where you'll see the summary of your text. As soon as "submit" button is pressed,
you'll see the timer in the "Summary" textbox. It shos: time spent this time/time spent last time.
  - The "Flag" button is to add info to dataset. It looks like that: Input Text,Upload .txt or .pdf file,Summary,timestamp


3) Example:
   - Text:
     Pseudastacus is an extinct genus of decapod crustaceans that lived during the Jurassic period in Europe, and possibly
    the Cretaceous period in Lebanon. Reaching up to 6 cm (2.4 in) in total length, Pseudastacus had a crayfish-like build,
    with long antennae, a triangular rostrum and a frontmost pair of appendages enlarged into pincers, with those of females
    being more elongated. There is evidence of possible gregarious behavior in P. lemovices in the form of multiple individuals
    preserved alongside each other, possibly killed in a mass mortality event. With the oldest known record dating to the
    Sinemurian age of the Early Jurassic, and possible species surviving into the Cenomanian stage of the Late Cretaceous,
    Pseudastacus has a long temporal range and was a widespread taxon. Fossils of this animal were first found in the Solnhofen
    Limestone of Germany, but have also been recorded from France, England and Lebanon. All species in this genus lived in marine habitats.
   - Summary:
       Pseudastacus is an extinct genus of decapod crustaceans that lived during the Jurassic period in Europe, and possibly the Cretaceous period
     in Lebanon. Reaching up to 6 cm (2.4 in) in total length, Pseudstacus had a crayfish-like build, with long antennae, a triangular rostrum and
     a frontmost pair of appendages enlarged into pincers.

4) Important Restrictions:
   - The model can only work with English! In the nearest future some other languages will be available but for now English only.
   - Once again, no .docx processing. The model works only with .pdf, .txt and manually inserted text.
