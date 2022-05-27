import { IsISO8601, IsNotEmpty, IsNumber, IsString } from "class-validator"

export class SaveCatchDto {
    @IsNumber()
    @IsNotEmpty()
    id_ves: number

    @IsNotEmpty()
    @IsISO8601()
    date: string

    @IsNumber()
    @IsNotEmpty()
    id_region: number

    @IsNumber()
    @IsNotEmpty()
    if_fish: number

    @IsNumber()
    @IsNotEmpty()
    catch_volume: number

    @IsNumber()
    @IsNotEmpty()
    id_regime: number

    @IsNumber()
    @IsNotEmpty()
    permit: number

    @IsNumber()
    @IsNotEmpty()
    id_owm: number

}