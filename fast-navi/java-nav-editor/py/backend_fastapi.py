from fastapi import FastAPI, Depends
from pydantic import BaseModel
import pymysql
from typing import List
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Java Nav Editor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"],  # 或 ["*"] 开发期
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= 数据库配置 =================
DB_CONFIG = dict(
    host="127.0.0.1",
    user="linjingu",
    password="linjingu",
    database="app",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)


def get_conn():
    return pymysql.connect(**DB_CONFIG)


# ================= 数据模型 =================
class NavData(BaseModel):
    id: int
    title: str


class LayoutItem(BaseModel):
    row_index: int
    col_index: int
    data_id: int

class LayoutSaveRequest(BaseModel):
    type: int
    layout: List[LayoutItem]


# ================= API =================

# @app.get("/api/nav/data", response_model=List[NavData])
def get_nav_data(type: int):
    """左侧素材区"""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title
                FROM java_nav_data
                WHERE deleted = 0 AND type = %s
                ORDER BY id
                """,
                (type,)
            )
            return cur.fetchall()
    finally:
        conn.close()


# @app.get("/api/nav/layout")
def get_layout(type: int):
    """加载布局"""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT l.row_index AS row_index,
                       l.col_index AS col_index,
                       d.id AS data_id,
                       d.title
                FROM java_nav_layout l
                JOIN java_nav_data d ON l.data_id = d.id
                WHERE l.type = %s
                ORDER BY l.row_index, l.col_index
                """,
                (type,)
            )
            return cur.fetchall()
    finally:
        conn.close()


@app.post("/api/nav/layout/save")
def save_layout(req: LayoutSaveRequest):
    items = req.layout
    layout_type = req.type
    print(layout_type, items)
    """保存布局（整 type 覆盖）"""
    if not items:
        return {"status": "empty"}

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM java_nav_layout WHERE type = %s", (layout_type,))

            sql = """
                INSERT INTO java_nav_layout (type, row_index, col_index, data_id)
                VALUES (%s, %s, %s, %s)
            """
            values = [
                (layout_type, i.row_index, i.col_index, i.data_id)
                for i in items
            ]
            cur.executemany(sql, values)

        conn.commit()
        return {"status": "ok", "count": len(items)}
    finally:
        conn.close()




# ========= 数据模型 =========
class SaveDiffPayload(BaseModel):
    type: int
    insert: List[LayoutItem]
    update: List[LayoutItem]
    delete: List[int]

# ========= 1. 左侧数据 =========
@app.get("/api/nav/data")
def get_nav_data(type: int):
    sql = """
        SELECT id, title
        FROM java_nav_data
        WHERE deleted = 0 AND type = %s
        ORDER BY id
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (type,))
            return cur.fetchall()
    finally:
        conn.close()

# ========= 2. 当前布局 =========
@app.get("/api/nav/layout")
def get_layout(type: int):
    sql = """
        SELECT data_id, row_index, col_index
        FROM java_nav_layout
        WHERE type = %s
        ORDER BY row_index, col_index
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (type,))
            return cur.fetchall()
    finally:
        conn.close()

# ========= 3. Diff 保存（核心） =========
@app.post("/api/nav/layout/save-diff")
def save_layout_diff(payload: SaveDiffPayload):
    conn = get_conn()
    try:
        conn.begin()
        with conn.cursor() as cur:

            # ---- delete ----
            if payload.delete:
                cur.execute(
                    """
                    DELETE FROM java_nav_layout
                    WHERE type = %s AND data_id IN (%s)
                    """ % (
                        payload.type,
                        ",".join(["%s"] * len(payload.delete))
                    ),
                    payload.delete
                )

            # ---- update ----
            for item in payload.update:
                cur.execute(
                    """
                    UPDATE java_nav_layout
                    SET row_index = %s, col_index = %s
                    WHERE type = %s AND data_id = %s
                    """,
                    (item.row_index, item.col_index, payload.type, item.data_id)
                )

            # ---- insert ----
            for item in payload.insert:
                cur.execute(
                    """
                    INSERT INTO java_nav_layout(type, data_id, row_index, col_index)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (payload.type, item.data_id, item.row_index, item.col_index)
                )

        conn.commit()
        return {"success": True}

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()


from typing import List, Optional

class SaveFullPayload(BaseModel):
    type: int
    grid: List[List[Optional[int]]]



@app.post("/api/nav/layout/save-full")
def save_layout_full(payload: SaveFullPayload):
    conn = get_conn()
    try:
        conn.begin()
        with conn.cursor() as cur:

            # 1️⃣ 读取旧布局，保留 style
            cur.execute(
                """
                SELECT data_id
                FROM java_nav_layout
                WHERE type = %s
                """,
                (payload.type,)
            )

            # 2️⃣ 删除当前 type 的所有布局（⚠️ 只删当前 type）
            cur.execute(
                "DELETE FROM java_nav_layout WHERE type = %s",
                (payload.type,)
            )

            # 3️⃣ 按最终 grid 重建（row/col 连续）
            for r, row in enumerate(payload.grid):
                for c, data_id in enumerate(row):
                    if data_id:
                        cur.execute(
                            """
                            INSERT INTO java_nav_layout
                              (type, data_id, row_index, col_index)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (
                                payload.type,
                                data_id,
                                r,
                                c
                            )
                        )

        conn.commit()
        return {"success": True}

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()


# ================= 启动 =================
# uvicorn backend_fastapi:app --reload --port 8000
