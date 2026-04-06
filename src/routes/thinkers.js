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
const {registrationValidation} = require('../validations/validations')
const bcryptjslibrary = require('bcryptjs')
const jwt = require('jsonwebtoken')
const verifyTK = require('../verifyTK')
const mongoose = require('mongoose')

var { ThinkerModel } = require("../models/Thinker");
var { TestThinkerModel } = require("../models/Thinker");
ThinkerModel.findOne()
TestThinkerModel.findOne()
Thinker = ThinkerModel


//Simple Post
router.post('/',async(req,res)=>{
    t_flag = req.get("test_flag")
    if(!t_flag){t_flag = "FALSE"}
    const test_flag = (t_flag.toUpperCase()=="TRUE")

    if(test_flag){
        Thinker = TestThinkerModel
    }
    var thinkerRole = "user"
    const req_admin_secret = req.get("admin_secret")
    if(!!req_admin_secret){
        if(req_admin_secret==process.env.ADMIN_SECRET){
            thinkerRole="admin"
            }else{
            return res.status(401).send({message:'Admin verification failed'})
            }
    }

    const {error} = registrationValidation(req.body)
    if(error){
        return res.status(400).send({message:error['details'][0]['message']})
    }

    const thinkerEmailExists = await Thinker.findOne({email:req.body.email})
    const thinkerUsernameExists = await Thinker.findOne({username:req.body.username})
    if(thinkerEmailExists||thinkerUsernameExists){
        return res.status(400).send({message:'Thinker username or email already exists'})
    }


    //If all ok so far - create hashed repr. of password
    const bcryptsalt = await bcryptjslibrary.genSalt(7)
    const hashedPW = await bcryptjslibrary.hash(req.body.password,bcryptsalt)

    const thinker = new Thinker({
        username:req.body.username,
        email:req.body.email,
        firstName:req.body.firstName,
        lastName:req.body.lastName,
        password:hashedPW,
        echoChambers:req.body.echoChambers,
        role:thinkerRole
    })


    try{
        const thinkerToSave = await thinker.save()
        res.send(thinkerToSave)
    }catch(err){
        res.status(400).send({message:err})
    }


})

router.get('/', verifyTK, async (req,res) =>{
    t_flag = req.get("test_flag")
    if(!t_flag){t_flag = "FALSE"}
    const test_flag = (t_flag.toUpperCase()=="TRUE")

    var getThinkerByLookup = await Thinker.findById(req.thinker._id)
    if(!getThinkerByLookup){
        Thinker = TestThinkerModel
        getThinkerByLookup = await Thinker.findById(req.thinker._id)
        Thinker = ThinkerModel
    }
    const admin_flag = (getThinkerByLookup.role.toUpperCase()=="ADMIN")

    //test use only for admins
    if(test_flag&&admin_flag){
        Thinker = TestThinkerModel
    }
    try {
        const thinker = await Thinker.find()
        res.send(thinker)
    } catch (error) {
        res.send({message:error})
    }
})

//Get2 where we find by UserID.
router.get('/:lookupValue',verifyTK, async(req,res) =>{
    const lookupValue = req.params.lookupValue

    t_flag = req.get("test_flag")
    if(!t_flag){t_flag = "FALSE"}
    const test_flag = (t_flag.toUpperCase()=="TRUE")

    var getThinkerByLookup = await Thinker.findById(req.thinker._id)
    if(!getThinkerByLookup){
        Thinker = TestThinkerModel
        getThinkerByLookup = await Thinker.findById(req.thinker._id)
        Thinker = ThinkerModel
    }
    const admin_flag = (getThinkerByLookup.role.toUpperCase()=="ADMIN")

    //test use only for admins
    if(test_flag&&admin_flag){
        Thinker = TestThinkerModel
    }
    try{
    var getThinkerByLookup = await Thinker.findOne({ username: lookupValue})
        if(!getThinkerByLookup){
            getThinkerByLookup = await Thinker.findOne({ email: lookupValue})
            if(!getThinkerByLookup){
                var validId = lookupValue.match(/^[a-f\d]{24}$/i)
                if(!validId){
                    return res.status(400).send({message:"Look up value is not a valid username, email or id"})
                    }
                    getThinkerByLookup = await Thinker.findById(req.params.lookupValue)
                    }
        }
        res.send(getThinkerByLookup)
    }catch(err){
        res.send({message:err})
    }
})

router.delete('/:thinkerId',verifyTK,async(req,res)=>{

    t_flag = req.get("test_flag")
    if(!t_flag){t_flag = "FALSE"}
    const test_flag = (t_flag.toUpperCase()=="TRUE")

    var getThinkerByLookup = await Thinker.findById(req.thinker._id)
    if(!getThinkerByLookup){
        Thinker = TestThinkerModel
        getThinkerByLookup = await Thinker.findById(req.thinker._id)
        Thinker = ThinkerModel
    }
    const admin_flag = (getThinkerByLookup.role.toUpperCase()=="ADMIN")

    //test use only for admins
    if(test_flag&&admin_flag){
        Thinker = TestThinkerModel
    }

    try{
        const unwantedThinker = await Thinker.findById(req.params.thinkerId)
        //return res.send({message: [unwantedThinker._id,req.thinker._id]})
        const isThinker = (unwantedThinker._id == req.thinker._id)
        if(!isThinker&&!admin_flag){
            return res.send({message:"You can only delete your own account!"})
        }
        const deleteThinkerById = await Thinker.deleteOne({_id:req.params.thinkerId})
        res.send(deleteThinkerById)
    }catch(err){
        res.send({message:err})
    }
})

router.delete('/',verifyTK,async(req,res)=>{

    t_flag = req.get("test_flag")
    if(!t_flag){t_flag = "FALSE"}
    const test_flag = (t_flag.toUpperCase()=="TRUE")

    var administrator = await Thinker.findById(req.thinker._id)
    if(!administrator){
        Thinker = TestThinkerModel
        administrator = await Thinker.findById(req.thinker._id)
        Thinker = ThinkerModel
    }

    const admin_flag = (administrator.role.toUpperCase()=="ADMIN")

    //test use only for admins
    if(test_flag&&admin_flag){
        Thinker = TestThinkerModel
    }
    //const access = req.thinker._id
    //return res.send({message:access})

    try{
        if(!admin_flag){
            return res.status(401).send({message:"Request lacks sufficient authentication credentials for the target resource"})
        }
        //return res.send({message:administrator._id})
        const deleteAllThinkers = await Thinker.deleteMany({
          _id: {$ne: administrator._id}
        })
        //const isThinker = (unwantedThinker._id == req.thinker._id) //debuging
        //const deleteThinkerById = await Thinker.deleteOne({_id:req.params.thinkerId}) //debuging
        res.send(deleteAllThinkers)

    }catch(err){
        res.send({message:err})
    }
})

module.exports = router