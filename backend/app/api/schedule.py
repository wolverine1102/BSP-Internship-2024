from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, date, timedelta
from app.db import create_connection


router = APIRouter()


def fetch_data_from_database():
    today = date.today()
    start_dtm = (
        today.strftime("%Y") + today.strftime("%m") + today.strftime("%d") + "0559"
    )

    tomorrow = today + timedelta(days=1)
    end_dtm = (
        tomorrow.strftime("%Y")
        + tomorrow.strftime("%m")
        + tomorrow.strftime("%d")
        + "0559"
    )

    fields = [
        "HEAT_NO",
        "ACT_CN_NO",
        "ACT_AR_NO",
        "ACT_VA_NO",
        "ACT_LF_NO",
        "ACT_RH_NO",
        "ACT_CC_NO",
        "TAPPING_STR_DTM",
        "TAPPING_END_DTM",
        "AR_STR_DTM",
        "AR_END_DTM",
        "VA_STR_DTM",
        "VA_END_DTM",
        "LF_STR_DTM",
        "LF_END_DTM",
        "RH_STR_DTM",
        "RH_END_DTM",
        "CC_STR_DTM",
        "CC_END_DTM",
    ]

    select_string = ""
    for i in range(len(fields)):
        if i == (len(fields) - 1):
            select_string += fields[i]
        else:
            select_string += f"{fields[i]}, "

    rows = None
    connection = create_connection()

    if connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT {select_string} 
                       FROM VW_SMS_HEAT 
                       WHERE blow_str_dtm > {start_dtm} AND blow_str_dtm < {end_dtm}"""
        )
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

    return rows


def modify_data(rows: list):
    schedule = []
    route_dict = {
        1: {"name": "CONV", "start_dtm_index": 7, "end_dtm_index": 8},
        2: {"name": "ARU", "start_dtm_index": 9, "end_dtm_index": 10},
        3: {"name": "VAD", "start_dtm_index": 11, "end_dtm_index": 12},
        4: {"name": "LF", "start_dtm_index": 13, "end_dtm_index": 14},
        5: {"name": "RH", "start_dtm_index": 15, "end_dtm_index": 16},
        6: {"name": "MC", "start_dtm_index": 17, "end_dtm_index": 18},
    }

    for row in rows:
        for row_index in range(1, 7):
            if row[row_index]:
                if row[route_dict[row_index]["end_dtm_index"]]:
                    schedule_dict = {
                        "heat_no": row[0],
                        "current_process": {
                            "name": route_dict[row_index]["name"],
                            "section": row[row_index],
                        },
                        "start_datetime": str(datetime.strptime(
                            row[route_dict[row_index]["start_dtm_index"]], "%Y%m%d%H%M"
                        )),
                        "end_datetime": str(datetime.strptime(
                            row[route_dict[row_index]["end_dtm_index"]], "%Y%m%d%H%M"
                        ))
                    }

                    schedule.append(schedule_dict)
            else:
                continue

    return schedule


@router.get("/schedule/")
async def index():
    rows = fetch_data_from_database()
    if rows:
        schedule = modify_data(rows)
        return JSONResponse(status_code=200, content=schedule)
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")