/*
The following sources were used as a template for the following route.
***************************************************************************************//*

*    Title: MiniFilm-node-auth source code
*    Author: Sotiriadis, S
*    Date: 2022
*    Code version: 2022
*    Availability: https://github.com/steliosot/MiniFilm-node-auth/blob/master/routes/auth.js
*
***************************************************************************************//*
(Version 2022) [Source code]. https://github.com/steliosot/MiniFilm-node-auth/blob/master/routes/auth.js

*/

const express = require('express')
const router = express.Router()

var { ThinkerModel } = require("../models/Thinker");
var { TestThinkerModel } = require("../models/Thinker");
ThinkerModel.findOne()
TestThinkerModel.findOne()
Thinker = ThinkerModel

const bcryptjslibrary = require('bcryptjs')
const jwt = require('jsonwebtoken')
const {signInValidation} = require('../validations/validations')

router.post('/',async(req,res)=>{
    t_flag = req.get("test_flag")
    if(!t_flag){t_flag = "FALSE"}
    const test_flag = (t_flag.toUpperCase()=="TRUE")

    if(test_flag=="TRUE"){
        Thinker = TestThinkerModel
    }

    const {error} = signInValidation(req.body)
    if(error){
        return res.status(400).send({message:error['details'][0]['message']})
    }

    thinker = await Thinker.findOne({email:req.body.email})
    if(!thinker){
        thinker = await Thinker.findOne({username:req.body.username})
    }

    if(!thinker){
        return res.status(400).send({message:'Thinker does not exist'})
    }

    const passwordValidation = await bcryptjslibrary.compare(req.body.password,thinker.password)
    if(!passwordValidation){
        return res.status(400).send({message:'Incorrect password, try again!'})
    }

    const jwtToken = jwt.sign({_id:thinker._id}, process.env.JWT_SECRET)
    res.header('auth-token',jwtToken).send({'auth-token':jwtToken})

})

module.exports = router