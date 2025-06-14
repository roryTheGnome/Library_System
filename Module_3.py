import pandas as pd
import requests as req


books = pd.read_excel('books.xlsx')

books['Biography'] = ''
books['Age Range'] = ''
books['Division'] = ''

valid_divs = {
    'romance', 'thriller', 'comedy', 'fantasy', 'science fiction', 'mystery',
    'historical', 'sci-fi', 'fan-fic', 'horror', 'utopian',
    'coming of age', 'psychological', 'family', 'adventure', 'dystopian',
    'biography', 'crime', 'legal', 'nonfiction','political',
    'action', 'drama', 'supernatural', 'natural'
}

def is_valid_subject(subject):
    s = subject.lower()
    return any(genre in s for genre in valid_divs)

#I choossed Open lib to work with
for i, row in books.iterrows():
    author = row['Name'] + ' ' + row['Surname']
    title = str(row['Title'])

    url = f"https://openlibrary.org/search.json?author={author}&title={title}"

    print(f"{title} by {author}") #here for debugginf purp

    try:
        response = req.get(url)
        if response.status_code != 200:
            print(f"Error with: {title}")
            continue

        data = response.json()
        docs = data.get('docs', [])

        if not docs:
            print(f"Upsi dupsi there is no docsy {title}")
            continue

        matched = None
        for doc in docs:
            if doc.get('title', '').lower() == title.lower() and author.lower() in ' '.join(doc.get('author_name', [])).lower():
                matched = doc
                break

        if not matched:
            print(f"Upsi dupsi there is no matchy {title}")
            continue

        work_key = matched.get('key')
        if not work_key:
            print("No key ?!?")
            continue

        work_url = f"https://openlibrary.org{work_key}.json" #i added another example response for this one in the end
        #i need this one cause i couldnt find anything division related in the first
        # idk what does it mean by division so i added the closest think i can to division which is subjecy

        repy = req.get(work_url)

        if repy.status_code != 200:
            print(f"Error: {repy.status_code}")
            continue

        work_data = repy.json()
        subjects = work_data.get('subjects', [])

        if subjects:

            filtered_subjects = [s for s in subjects if is_valid_subject(s)]

            if filtered_subjects:

                books.at[i, 'Division'] = ', '.join(filtered_subjects[:3])

        # as far as i understand there is no age range related data in open lib
        # (i added an example response in the end of this file)

        author_keys = matched.get('author_key', [])
        if author_keys:

            author_url = f"https://openlibrary.org/authors/{author_keys[0]}.json"
            bio_response = req.get(author_url)

            if bio_response.status_code == 200:

                author_data = bio_response.json()
                bio = author_data.get('bio')

                if isinstance(bio, dict):

                    bio = bio.get('value', '')

                books.at[i, 'Biography'] = bio

    except Exception as e:
        print(f"Failed on {title}: {e}")

books.to_excel('books_with_extended_data.xlsx', index=False)

'''
Thing to add:
- The division that published the book 
- Author’s biography 
- Suggested age range
'''

"""
Additioanled installs i had for this Module:
pip install requests
"""

"""
{
    "numFound": 3,
    "start": 0,
    "numFoundExact": true,
    "num_found": 3,
    "documentation_url": "https://openlibrary.org/dev/docs/api/search",
    "q": "",
    "offset": null,
    "docs": [
        {
            "author_key": [
                "OL19981A"
            ],
            "author_name": [
                "Stephen King"
            ],
            "cover_edition_key": "OL27306907M",
            "cover_i": 10712767,
            "ebook_access": "printdisabled",
            "edition_count": 28,
            "first_publish_year": 2019,
            "has_fulltext": true,
            "ia": [
                "elinstitutounano0000king",
                "institutenovel0000king_s5n8",
                "institute0000king_m4p7",
                "institutenovel0000king",
                "institute0000king",
                "institutenovel0000king_h5y0",
                "institutenovel0000step",
                "isbn_9789022587423"
            ],
            "ia_collection_s": "internetarchivebooks;printdisabled",
            "key": "/works/OL20126932W",
            "language": [
                "dut",
                "eng",
                "fre",
                "spa"
            ],
            "public_scan_b": false,
            "title": "The Institute"
        },
        {
            "author_key": [
                "OL11414296A"
            ],
            "author_name": [
                "R. K.; Stephen King-Hall Ullmann"
            ],
            "ebook_access": "no_ebook",
            "edition_count": 1,
            "first_publish_year": 1954,
            "has_fulltext": false,
            "key": "/works/OL31249395W",
            "public_scan_b": false,
            "title": "GERMAN PARLIAMENTS. A Study of the Development of Representative Institutions in Germany."
        },
        {
            "author_key": [
                "OL12256153A"
            ],
            "author_name": [
                "King-Hall, Stephen, and Ullmann, Richard K."
            ],
            "ebook_access": "no_ebook",
            "edition_count": 1,
            "first_publish_year": 1954,
            "has_fulltext": false,
            "key": "/works/OL33860684W",
            "public_scan_b": false,
            "title": "German Parliaments a Study of the Development of Representative Institutions in Germany"
        }
    ]
}
""" #example response 1

""""
{
  "description": "In the middle of the night, in a house on a quiet street in suburban Minneapolis, intruders silently murder Luke Ellis’s parents and load him into a black SUV. The operation takes less than two minutes. Luke will wake up at The Institute, in a room that looks just like his own, except there’s no window. And outside his door are other doors, behind which are other kids with special talents—telekinesis and telepathy—who got to this place the same way Luke did: Kalisha, Nick, George, Iris, and ten-year-old Avery Dixon. They are all in Front Half. Others, Luke learns, graduated to Back Half, “like the roach motel,” Kalisha says. “You check in, but you don’t check out.”\r\n\r\nIn this most sinister of institutions, the director, Mrs. Sigsby, and her staff are ruthlessly dedicated to extracting from these children the force of their extranormal gifts. There are no scruples here. If you go along, you get tokens for the vending machines. If you don’t, punishment is brutal. As each new victim disappears to Back Half, Luke becomes more and more desperate to get out and get help. But no one has ever escaped from the Institute.\r\n\r\nAs psychically terrifying as Firestarter, and with the spectacular kid power of It, The Institute is Stephen King’s gut-wrenchingly dramatic story of good vs. evil in a world where the good guys don’t always win.",
  "title": "The Institute",
  "key": "/works/OL20126932W",
  "authors": [
    {
      "author": {
        "key": "/authors/OL19981A"
      },
      "type": {
        "key": "/type/author_role"
      }
    }
  ],
  "type": {
    "key": "/type/work"
  },
  "links": [
    {
      "title": "StephenKing.com - The Institute",
      "url": "https://www.stephenking.com/library/novel/institute_the.html",
      "type": {
        "key": "/type/link"
      }
    },
    {
      "title": "The Institute (novel) - Wikipedia",
      "url": "https://en.wikipedia.org/wiki/The_Institute_(novel)",
      "type": {
        "key": "/type/link"
      }
    },
    {
      "title": "The Institute by Stephen King review – return to DuPray",
      "url": "https://www.theguardian.com/books/2019/sep/04/the-institute-stephen-king-review",
      "type": {
        "key": "/type/link"
      }
    },
    {
      "title": "The Institute | Stephen King Wiki | FANDOM powered by Wikia",
      "url": "https://stephenking.fandom.com/wiki/The_Institute",
      "type": {
        "key": "/type/link"
      }
    },
    {
      "title": "‘The Institute’ Might Be Stephen King’s Scariest Novel Yet",
      "url": "https://www.nytimes.com/2019/09/10/books/review/stephen-king-the-institute.html",
      "type": {
        "key": "/type/link"
      }
    },
    {
      "title": "'The Institute,' by Stephen King book review - The Washington ...",
      "url": "https://www.washingtonpost.com/entertainment/books/stephen-kings-the-institute-turns-our-political-moment-into-gripping-horror/2019/09/09/fae7d094-cf52-11e9-87fa-8501a456c003_story.html",
      "type": {
        "key": "/type/link"
      }
    },
    {
      "title": "Déjà vu Destroyed: On Stephen King’s “The Institute”",
      "url": "https://lareviewofbooks.org/article/deja-vu-destroyed-on-stephen-kings-the-institute/",
      "type": {
        "key": "/type/link"
      }
    },
    {
      "title": "Review: The Institute by Stephen King | The Nerd Daily",
      "url": "https://www.thenerddaily.com/review-the-institute-stephen-king/",
      "type": {
        "key": "/type/link"
      }
    },
    {
      "title": "New York Times review",
      "url": "https://www.nytimes.com/2019/09/08/books/review-institute-stephen-king.html",
      "type": {
        "key": "/type/link"
      }
    }
  ],
  "covers": [10712767, -1, 12302898, 12331444, 14060864, 14060865],
  "subject_places": [
    "Minneapolis",
    "Institute",
    "Front Half",
    "Back Half",
    "Florida",
    "DuPray",
    "South Carolina"
  ],
  "subjects": [
    "fiction",
    "thrillers",
    "supernatural",
    "suspense",
    "horror",
    "missing children",
    "psychic ability",
    "child abuse",
    "kidnapping",
    "kidnapping victims",
    "parapsychology",
    "Fiction, horror",
    "Missing persons, fiction",
    "South carolina, fiction",
    "Fiction, science fiction, general",
    "American literature",
    "nyt:combined-print-and-e-book-fiction=2019-09-29",
    "New York Times bestseller",
    "New York Times reviewed",
    "Fiction, thrillers, suspense",
    "FICTION / Thrillers / Suspense",
    "FICTION / Horror",
    "FICTION / Thrillers / Supernatural",
    "Horror fiction",
    "Fiction, thrillers, psychological"
  ],
  "subject_people": [
    "Luke Ellis",
    "Kalisha",
    "Nick",
    "George",
    "Iris",
    "Avery Dixon",
    "Mrs. Sigsby",
    "Tim Jamieson"
  ],
  "subject_times": [
    "2017-2019"
  ],
  "excerpts": [
    {
      "excerpt": "Half an hour after Tim Jamieson's Delta flight was scheduled to leave Tampa for the bright lights and tall buildings of New York, it was still parked at the gate.",
      "comment": "first sentence",
      "author": {
        "key": "/people/seabelis"
      }
    }
  ],
  "latest_revision": 11,
  "revision": 11,
  "created": {
    "type": "/type/datetime",
    "value": "2019-09-10T15:08:53.121200"
  },
  "last_modified": {
    "type": "/type/datetime",
    "value": "2024-08-19T13:20:58.165114"
  }
}
""" #example response 2