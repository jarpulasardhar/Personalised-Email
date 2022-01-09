
# importing required libraries
import smtplib
import csv
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# returns the template object containing the contents of the template.txt file
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def main():
    message_template = read_template('template.txt')

    # input the email details
    MY_ADDRESS = input("Enter your mail id : ")
    PASSWORD = input("Enter Password : ")

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # reading file as context manager so not to worry about closing the file in the end.
    with open("details.csv", 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # the below statement will skip the first row
        next(csv_reader)

        for lines in csv_reader:
            msg = MIMEMultipart()  # create a message

            # add in the actual person name to the message template
            message = message_template.substitute(PERSON_NAME=lines[0], MATH=lines[2], ENG=lines[3], SCI=lines[4])
            print(message)

            # setup the parameters of the message
            msg['From'] = MY_ADDRESS
            msg['To'] = lines[1]
            msg['Subject'] = "Mid term grades"

            # add in the message body
            msg.attach(MIMEText(message, 'plain'))

            # send the message via the server set up earlier.
            s.send_message(msg)
            del msg

    # Terminate the SMTP session and close the connection
    s.quit()


if __name__ == '__main__':
    main()
