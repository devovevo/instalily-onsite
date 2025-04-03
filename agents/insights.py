from openai import OpenAI, RateLimitError, OpenAIError
import backoff

client = OpenAI()

@backoff.on_exception(backoff.expo, (RateLimitError, OpenAIError))
def gen(text):
    return client.responses.create(
        model="gpt-4o",
        input=f"You are an agent for a roofing distribution company which is trying to sell roofing products to roofing contractors. The below text is about a roofing contractor's website, and you're job is to take that information and try to find actionable insights that would help the distributor sell roofing products to that specific contractor. Your insights should help a salesperson focus their pitch on what specific products the contractor might need, what price they could be sold at, what services they provide, and how receptive they would be to a new distributor. Be as brief as possible (only including very relevant information) and answer in bullet points.\nTEXT STARTS BELOW THIS LINE\n{text}",
    ).output_text