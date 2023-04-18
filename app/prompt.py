import logging
from llama_index.prompts.prompts import QuestionAnswerPrompt

QUESTION_ANSWER_PROMPT_TMPL_CN = (
    "上下文信息如下所示： \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "我的问题是：{query_str}\n"
)

QUESTION_ANSWER_PROMPT_TMPL_EN = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "My question is {query_str}\n"
)

def get_prompt_template(language='zh'):
    if language == 'en':
        logging.info('=====> Use English prompt template!')
        return QuestionAnswerPrompt(QUESTION_ANSWER_PROMPT_TMPL_EN)
    else:
        logging.info('=====> Use Chinese prompt template!')
        return QuestionAnswerPrompt(QUESTION_ANSWER_PROMPT_TMPL_CN)