# Mossquito

Mossquito is a notebook preprocessor that extracts notebook contents and convert it into python script. This app is used by instructors of Hacktiv8 Indonesia's Data Science bootcamp program to extract and convert student assigments, that are mostly in notebook formats, into python scripts. This app also uses MOSS for plagiarism checking.

> Mossquito is inspired by **Park Ye-Joo**'s article about "_Run MOSS Plagiarism Checker on Jupyter Notebooks_" in his personal blog.

## Requirements

- MOSS access
  - You can obtain MOSS access ([here](https://theory.stanford.edu/~aiken/moss/))

## Use Case

### Use Case 1 - Only extract and convert notebook to scripts

```shell
python main.py <your_assigment_directory>
```

### Use Case 2 - Running full pipeline (extract ➡️ convert ➡️ moss checking)

```shell
./run.sh <your_assignment_directory>
```

## Reference

- [Run MOSS Plagiarism Checker on Jupyter Notebooks](https://park.is/blog_posts/20230420_running_moss_plagiarism_checker)
  by Park Ye-Joo
