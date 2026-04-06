/*
The following sources were used as a template for the following route.
***************************************************************************************//*

*    Title: MiniFilm-node-auth source code
*    Author: Sotiriadis, S
*    Date: 2022
*    Code version: 2022
*    Availability: https://github.com/steliosot/MiniFilm-node-auth/blob/master/validations/validation.js
*
***************************************************************************************//*
(Version 2022) [Source code]. https://github.com/steliosot/MiniFilm-node-auth/blob/master/validations/validation.js
*/


const joi = require('joi')

//TODO Include validations here
const signInValidation = (dataToValidate) =>{
    const validateData = joi.object({
        email:joi.string().min(4).max(320).email(),
        username:joi.string().min(4).max(12),
        password:joi.string().required().min(6).max(32)
    })
    return validateData.validate(dataToValidate)
}

const registrationValidation = (dataToValidate) =>{
    const validateData = joi.object({
        username:joi.string().required().min(4).max(12),
        email:joi.string().required().min(4).max(320).email(),
        password:joi.string().required().min(6).max(32),
        firstName:joi.string().required().min(1).max(32),
        lastName:joi.string().required().min(1).max(32),
        echoChambers:joi.array().required()
    })
    return validateData.validate(dataToValidate)
}

const commentValidation = (dataToValidate) =>{
    const validateData = joi.object({
        detail:joi.string().required().min(4).max(400),
    })
    return validateData.validate(dataToValidate)
}

const thoughtValidation = (dataToValidate) =>{
    const validateData = joi.object({
        title:joi.string().required().min(4).max(75),
        description:joi.string().required().min(4).max(140),
        detail:joi.string().required().min(4).max(800),
        echoChamber:joi.string().required().min(1).max(32),
        image:joi.string().uri(),
    })
    return validateData.validate(dataToValidate)
}

module.exports.signInValidation = signInValidation
module.exports.registrationValidation = registrationValidation
module.exports.commentValidation = commentValidation
module.exports.thoughtValidation = thoughtValidation