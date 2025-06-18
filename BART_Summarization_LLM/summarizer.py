"""Here is provided program code creating a summarization model. You'll see some explanations
on some engineering ideas as well. The text in large comment sections is aimed at giving
extended explanations on what's actually going on in the code, small comment sections provide
some short information on what can be a bit confusing"""


#importing necessary libraries
from transformers import BartForConditionalGeneration, BartTokenizer
import nltk
from nltk.tokenize import sent_tokenize
import logging

#setting up a loger so that it's possible to display processing info (i.e. "starting summarization")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#need to download "punkt" to tokenize text
nltk.download('punkt')


"""A decision was made to create a TextSummarizer class so that it will be easy to create 
a LLM agent. Text preprocessing functions are provided. This way the model can work with
large texts without any problems. The model chosen is bart but in the nearest future 
I'm going to add some other models like T-5 or T-5-large so that the user will have some
variety in summaries and will be able to choose the most appropriate one for his goals"""


class TextSummarizer:

    #initializing the model(bart is used)
    def __init__(self, model_name="facebook/bart-large-cnn"):
        logger.info(f"The model being loaded is {model_name}")
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.model = BartForConditionalGeneration.from_pretrained(model_name)

        #bart's max input length is 1024, so setting slightly less to make sure we won't have any issues
        self.max_input_length = 1000

        #setting max summary length of temporary summaries, so that final summary would be compact and informative
        self.max_summary_length = 150

        #setting min summary length so that summary wouldn't be very short^-^
        self.min_summary_length = 60

    """The idea of working with large texts is to split them into so called 'chunks'. At first I'm gonna
    tokenize the whole text so as to get sentences, for every sentence count a number of tokens, and while 
    total number of tokens is less than max_input_length I'll append them to a chunk so the whole text will 
    be split into some parts (chunks) for further processing"""

    def text2chunks(self, text):
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0


        for sentence in sentences:

            #counting tokens
            sentence_tokens = self.tokenizer.encode(sentence, add_special_tokens=False)
            sentence_length = len(sentence_tokens)

            #checking whether to append sentence to an existing chunk or start a new chunk
            if current_length + sentence_length >= self.max_input_length:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length

            else:
                current_chunk.append(sentence)
                current_length += sentence_length

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        logger.info(f"Text will be split into {len(chunks)} chunks")
        return chunks


    """As the text was divided into chunks, I'll summarize each part separately. This way 
    the model will just combine summaries of text parts. It's the best idea that came to my mind, 
    but i believe there are some better ways, thus still investigating how to manage this better^-^"""


    def summarize_chunk(self, text):
        #tokenizing text and returning it as pytorch tensors
        inputs = self.tokenizer(text, return_tensors="pt", max_length=self.max_input_length, truncation=True)

        #generate() method creates summary
        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_length=self.max_summary_length, #max summary length
            min_length=self.min_summary_length, #min summary length
            length_penalty=2.0, #less penalty for long summaries
            num_beams=4, #using beam search for quality improvement
            early_stopping=True #stop when summary is stable
        )

        #last step is decoding summary
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

    """Summarize method is here to combine all the intermediate summaries. Additionally 
    raising exceptions when something is wrong(i.e. issues loading the text). Moreover I guess it's
    necessary to shorten final summary if it's too long, so I'll summarize the summary in this case.
    Logging is provided as well"""

    def summarize(self, text):
        #checking if text is not empty
        if not text.strip():
            raise ValueError("Seems like an error occurred...Check whether the input is not empty")
        #dividing text into chunks
        chunks = self.text2chunks(text)

        #checking if dividing into chunks is successful
        if not chunks:
            raise ValueError("Seems like an error occurred...Can't split text into chunks")

        intermediate_summaries = []

        #creating intermediate summaries
        for i, chunk in enumerate(chunks):
            logger.info(f"Chunk summarization in progress... {i+1}/{len(chunks)}")
            summary = self.summarize_chunk(chunk)
            intermediate_summaries.append(summary)

        #combining intermediate summaries
        combined_summary = " ".join(intermediate_summaries)

        combined_tokens = len(self.tokenizer.encode(combined_summary))

        #checking if combined summary is not too large
        if combined_tokens > self.max_input_length:
            logger.info("Combining chunks summaries...")
            final_summary = self.summarize_chunk(combined_summary)
        else:
            final_summary = combined_summary

        return final_summary