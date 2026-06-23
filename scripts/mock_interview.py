import random


def generate_mock_questions():

    questions = [

        "Explain OSI Model.",

        "What is the difference between TCP and UDP?",

        "What is VLAN?",

        "Explain DHCP process.",

        "What is DNS?",

        "What is a Firewall?",

        "What is SIEM?",

        "Explain Network Monitoring.",

        "What is Routing?",

        "What is Python Automation in Networking?"

    ]

    return random.sample(
        questions,
        5
    )


def evaluate_answers(
        answers
):

    score = 0

    feedback = []

    for answer in answers:

        if len(
            answer.strip()
        ) > 50:

            score += 20

        else:

            feedback.append(

                "Provide more detailed answers."

            )

    score = min(
        score,
        100
    )

    return {

        "score":
        score,

        "feedback":
        feedback
    }