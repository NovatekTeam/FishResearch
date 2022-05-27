import { Type } from "class-transformer"
import {   IsNotEmpty, IsNumber } from "class-validator"


export class SaveCatchDto {
    @IsNumber()
    @IsNotEmpty()
    @Type(() => Number)
    id_ves: number
   
    @IsNotEmpty()
    @Type(() => Date)
    date: Date

    @IsNumber()
    @IsNotEmpty()
    @Type(() => Number)
    id_region: number

    @IsNumber()
    @IsNotEmpty()
    @Type(() => Number)
    id_fish: number

    @IsNumber()
    @IsNotEmpty()
    @Type(() => Number)
    catch_volume: number

    @IsNumber()
    @IsNotEmpty()
    @Type(() => Number)
    id_regime: number

    @IsNumber()
    @IsNotEmpty()
    @Type(() => Number)
    permit: number

    @IsNumber()
    @IsNotEmpty()
    @Type(() => Number)
    id_own: number

}