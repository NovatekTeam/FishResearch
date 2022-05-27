import { Injectable } from "@nestjs/common";
import { PrismaService } from "src/prisma/prisma.service";
import * as csv from '@fast-csv/parse'
import { SaveCatchDto } from "./dto/save-catch.dto";

@Injectable()
export class CatchService {
    constructor(private prisma: PrismaService){}

    loadCatchDictRow(dto: SaveCatchDto){
        return dto
    }

    loadCatchDictRows(dto: SaveCatchDto[]){
        return dto
    }

    loadCsv(file: Express.Multer.File){
        csv.parseFile(file.path,{delimiter: ';' , headers: true})
        .on('error', error => console.log(error))
        .on('data', row => console.log(row))
    }


}