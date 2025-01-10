# Data scraper for major requirements 📝
An application to parse major requirements data into easily readable Excel Spreadsheets

## How it was made:
- Python 🐍
- BeautifulSoup4 🥣
- pandas 🐼
- requests ♻️
- CSV 📝

## Why it was made:
- Created for UBC LFS to help the Learning Centre team 🌱

## Way I structured data for faster parsing
- Hashmap → Hashmap → Set (easy dup checking)
```javascript
    major_content = {
        "Applied Biology": {
            "Applied Animal Biology": {"Course 1", "Course 2"}
            "Sustainable Agriculture and Environment": {"Course 1", "Course 2"}
        },
        "Food, Nutrition and Health": {
            "Dietetics": {"Course 1", "Course 2"},
            "Food Market Analysis": {"Course 1", "Course 2"},
            "Food Science": {"Course 1", "Course 2"},
            "Nutritional Sciences": {"Course 1", "Course 2"},
            "Food and Nutritional Sciences": {"Course 1", "Course 2"},
            "Food, Nutrition and Health": {"Course 1", "Course 2"}
        }
    }
   
```
