## https://thepythoncode.com/article/reading-emails-in-python for template

import email
import imaplib

def update_saved_content():
    with open("config") as f:
        lines = f.read().split("\n")
        f.close()
        username     = lines[0]
        password     = lines[1]
        imap_addr    = lines[2]
        trusted_addr = lines[3]

        imap = imaplib.IMAP4_SSL(imap_addr)
        imap.login(username, password)

        status, ms = imap.select("INBOX")
        num_messages = int(ms[0])

        ## fetch most recent / check it's the right email
        res, msg = imap.fetch(str(num_messages),"(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])

                # decode the email subject
                subject, encoding = email.header.decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)

                # check it is from the trusted sender
                sender, encoding = email.header.decode_header(msg.get("From"))[0]
                if isinstance(sender, bytes):
                    sender = sender.decode(encoding)

                # extract just the address from the From field (ignore the display name)
                if sender[sender.index("<")+1:-1] == trusted_addr:

                    ## Decode the email contents / update stored message
                    if msg.is_multipart():
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                ## update stored message
                                with open("curr_message.txt", "w") as f2:
                                    f2.write(body)
                                    f2.close()

                            elif "attachment" in content_disposition:
                                # download attachment
                                filename = part.get_filename()
                                if filename:
                                    open("../curr_img."+filename.split(".")[-1], "wb").write(part.get_payload(decode=True))

                    else:
                        print("non-multipart messages not supported")
                else:
                    print(f"sender {sender} is not the trusted sender; ignoring email")


if __name__ == "__main__":
    update_saved_content()