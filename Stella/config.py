#    Stella (Development)
#    Copyright (C) 2021 - meanii (Anil Chauhan)
#    Copyright (C) 2021 - SpookyGang (Neel Verma, Anil Chauhan)

#    This program is free software; you can redistribute it and/or modify 
#    it under the terms of the GNU General Public License as published by 
#    the Free Software Foundation; either version 3 of the License, or 
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from os import getenv

from dotenv import load_dotenv

if os.path.exists("stella.env"):
    load_dotenv("stella.env")
else:
    load_dotenv()

class Config:
    API_ID =  int(getenv("API_ID", "4277083"))
    API_HASH = getenv("API_HASH", "bb0ddae0921fc020ce61faae2d1261d5")

    OWNER_ID = int(getenv("OWNER_ID", "5497627952"))
    
    BOT_TOKEN = getenv("BOT_TOKEN", "6352046929:AAGm8WgIgpJnHvQzI4dnn_d6XP91rIO-Y3M")
    BOT_NAME = getenv("BOT_NAME", "Elisa")
    BOT_USERNAME= getenv("BOT_USERNAME", "AlexamachineRobot")
    BOT_ID = getenv("BOT_ID", "5643681960")
    PREFIX = getenv("PRRFIX", "/")
    MONGO_URL = getenv("MONGO_URL", "mongodb+srv://devilking:2301820k@cluster1.fmtgisg.mongodb.net/?retryWrites=true&w=majority")
    DATABASE_URI = getenv("DATABASE_URI", "mongodb+srv://devilking:2301820k@cluster1.fmtgisg.mongodb.net/?retryWrites=true&w=majority")
    BACKUP_CHAT = getenv("BACKUP_CHAT", "-1001590206395")

    LOG_CHANNEL = getenv("LOG_CHANNEL", None)

    SUDO_USERS = list(map(int, getenv("SUDO_USERS", "5497627952").split()))


    # APIs 
    StellaGbanAPI = getenv("StellaGbanAPI", None)
    
