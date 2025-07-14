import pandas as pd 

from fastapi import APIRouter

from models.request import DiscussionBoardRequest
from models.response import DiscussionBoardResponse 

from utils.data_loader import topics, entries, courses, users

router = APIRouter()


@router.post("/discussion-board", response_model = DiscussionBoardResponse)
def get_discussion_board(data: DiscussionBoardRequest) -> DiscussionBoardResponse:

    """
    Returns the discussion board contents
    """
    course_code = data.course_code

    #Merge DataFrame
    merged_df = topics \
        .merge(entries, on="topic_id", how="left") \
        .merge(courses, on="course_id", how="left") \
        .merge(
            users,
            left_on='entry_posted_by_user_id',
            right_on='user_id',
            how='left'
        )

    # Filter DataFrame
    filtered_df = merged_df[merged_df['course_code'] == course_code]
    filtered_df = filtered_df[['topic_id', 'topic_title', 'topic_content', 'entry_content', 'entry_created_at', 'user_name']]
    
    # Convert to dt object
    filtered_df['entry_created_at'] = pd.to_datetime(filtered_df['entry_created_at'])
    
    #Sort values by earliest
    grouped = filtered_df.sort_values('entry_created_at').groupby(['topic_id', 'topic_title','topic_content'])

    topics_list = []
    for (topic_id, topic_title, topic_content), group_df in grouped:
        list_of_entries = group_df[['entry_content', 'entry_created_at', 'user_name']] \
            .dropna(subset=['entry_content']) \
            .to_dict(orient='records')
        
        topics_list.append({
            "topic_id": topic_id,
            "topic_title": topic_title,
            "topic_content": topic_content,
            "entries": list_of_entries
        })

    return DiscussionBoardResponse(topics=topics_list)