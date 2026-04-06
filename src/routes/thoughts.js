/*
The following sources were used as a template for the following route.
***************************************************************************************//*

*    Title: MiniFilm-node-auth source code
*    Author: Sotiriadis, S
*    Date: 2022
*    Code version: 2022
*    Availability: https://github.com/steliosot/MiniFilm-node-auth/blob/master/routes/films.js
*
***************************************************************************************//*
(Version 2022) [Source code]. https://github.com/steliosot/MiniFilm-node-auth/blob/master/routes/films.js

*/

const express = require('express')
const router = express.Router()
const verifyTK = require('../verifyTK')

const {commentValidation} = require('../validations/validations');
const {thoughtValidation} = require('../validations/validations');

var { CommentModel } = require("../models/Comment");
var { TestCommentModel } = require("../models/Comment");
CommentModel.findOne()
TestCommentModel.findOne()
Comment = CommentModel

var { ThoughtModel } = require("../models/Thought");
var { TestThoughtModel } = require("../models/Thought");
ThoughtModel.findOne()
TestThoughtModel.findOne()
Thought = ThoughtModel

var { ThinkerModel } = require("../models/Thinker");
var { TestThinkerModel } = require("../models/Thinker");
ThinkerModel.findOne()
TestThinkerModel.findOne()
Thinker = ThinkerModel


//Simple Post
router.post('/',verifyTK,async(req,res)=>{

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


    if(test_flag&&admin_flag){
        Comment = TestCommentModel
        Thought = TestThoughtModel
        Thinker = TestThinkerModel
    }

    const {error} = thoughtValidation(req.body)
    if(error){
        return res.status(400).send({message:error['details'][0]['message']})
    }

    const postThought = new Thought({
        title:req.body.title,
        timestamp:req.body.timestamp,
        thinker:req.thinker, //once the request is authenticated (verifyTK, a "thinker" field is added to the request with the authenticated user id)
        description:req.body.description,
        detail:req.body.detail,
        echoChamber:req.body.echoChamber,
        //score:'starting score will always be 0'
        image:req.body.image
    })



    try{
        const thoughtToSave = await postThought.save()
        res.send(thoughtToSave)
    }catch(err){
        res.send({message:err})
    }


})

// Simple Get
router.get('/',verifyTK, async (req,res) =>{

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

    //testing only available to admins
    if(test_flag&&admin_flag){
        Comment = TestCommentModel
        Thought = TestThoughtModel
        Thinker = TestThinkerModel
    }

    try {
        const thought = await Thought.find().sort({"score":-1,"timestamp":-1})
        res.send(thought)
    } catch (error) {
        res.send({message:error})
    }
})

//Get2 where we find by ID.
router.get('/:thoughtId',verifyTK, async(req,res) =>{
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

    if(test_flag&&admin_flag){
        Comment = TestCommentModel
        Thought = TestThoughtModel
        Thinker = TestThinkerModel
    }

    try{
        const getThoughtById = await Thought.findById(req.params.thoughtId)
        res.send(getThoughtById)

    }catch(err){
        res.send({message:err})
    }
})

router.get('/:thoughtId/comments',verifyTK, async(req,res) =>{

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

    if(test_flag&&admin_flag){
        Comment = TestCommentModel
        Thought = TestThoughtModel
        Thinker = TestThinkerModel
    }

    try{
        const getThoughtById = await Thought.findById(req.params.thoughtId)
        const commentsById = await Comment.find({
            '_id': { $in: getThoughtById.comments}
        }).sort({"timestamp":-1})
        return res.send({comments:commentsById})
        res.send(getThoughtById)

    }catch(err){
        res.send({message:err})
    }
})


router.patch('/:actionId/:thoughtId',verifyTK, async(req,res)=>{
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

    if(test_flag&&admin_flag){
        Comment = TestCommentModel
        Thought = TestThoughtModel
        Thinker = TestThinkerModel
    }

    try{

        const oldThought = await Thought.findById(req.params.thoughtId)
        if(req.thinker._id==oldThought.thinker){
            return res.status(403).send({message:"Don't be weird, you can't like or comment on your own thoughts!"})
        }


        newComment = oldThought.comments
        newScoreCount = oldThought.score

        const action = req.params.actionId
        if(action=="comment"){
            const reqComment = new Comment({
                thinker:req.thinker._id,
                detail:req.body.comment
            })
            const {error} = commentValidation({detail:req.body.comment})
            if(error){
                return res.status(400).send({message:error['details'][0]['message']})
            }
        try{
            const commentToSave = await reqComment.save()
            //res.send(thoughtToSave)
        }catch(err){
            res.send({message:err})
        }
        newComment = [...oldThought.comments, reqComment]
    }

        if(action=="like"){
            newScoreCount = newScoreCount + 1
        }

        const updateThoughtById = await Thought.updateOne(
            {_id:req.params.thoughtId},
            {$set:{
                title:oldThought.title,
                timestamp:oldThought.timestamp,
                thinker:oldThought.thinker,
                description:oldThought.description,
                detail:oldThought.detail,
                echoChamber:oldThought.echoChamber,
                score:newScoreCount,
                image:oldThought.image,
                comments:newComment
                }
            }
        )
        res.send(updateThoughtById)
    }catch(err){
        res.send({message:err})
    }
})

    router.delete('/:thoughtId',verifyTK,async(req,res)=>{
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

    if(test_flag&&admin_flag){
        Comment = TestCommentModel
        Thought = TestThoughtModel
        Thinker = TestThinkerModel
    }

    try{
        const unwantedThought = await Thought.findById(req.params.thoughtId)
        //return res.send({message: [unwantedThought.thinker,req.thinker._id]})
        const isThinkersThought = (unwantedThought.thinker == req.thinker._id)
        if(!isThinkersThought&&!admin_flag){
            return res.send({message:"You can't delete other people's thoughts!"})
        }
        const deleteThoughtById = await Thought.deleteOne({_id:req.params.thoughtId})
        res.send(deleteThoughtById)
    }catch(err){
        res.send({message:err})
    }
})

router.delete('/',verifyTK,async(req,res)=>{
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

    if(test_flag&&admin_flag){
        Comment = TestCommentModel
        Thought = TestThoughtModel
        Thinker = TestThinkerModel
    }

    try{
        if(!admin_flag){
            return res.status(401).send({message:"Request lacks sufficient authentication credentials for the target resource"})
        }
        //return res.send({message:administrator._id})
        const deleteAllThoughts = await Thought.deleteMany({})
        const deleteAllComments = await Comment.deleteMany({})
        return res.send({thoughtsDelete: deleteAllThoughts, commentsDelete:deleteAllComments})

    }catch(err){
        res.send({message:err})
    }
})

module.exports = router