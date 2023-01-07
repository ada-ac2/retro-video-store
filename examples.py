# @rentals_bp.route("/check-out", methods=["POST"])
# def checkout_video():
#     checkout_data = request.get_json()

#     try:
#         customer = Customer.query.get(checkout_data["customer_id"])
#         video = Video.query.get(checkout_data["video_id"])
#     except KeyError as err:
#         abort(make_response({"message":f"Missing {err.args[0]}."}, 400))
    
#     if not customer:
#         abort(make_response({"message":f"Customer does not exist."}, 404))

#     if not video:
#         abort(make_response({"message":f"Video does not exist."}, 404))
    
#     rentals = Rental.query.all()
    
#     rental_count = 0
#     for rental in rentals:
#         if rental.customer_id == customer.id and rental.video_id == video.id:
#             abort(make_response({"message":f"Customer {customer.id} is already renting video {video.id}."}, 400))

#         if rental.video_id == video.id:
#             rental_count += 1

#     available_inventory = video.total_inventory - rental_count
#     if available_inventory <= 0:
#         abort(make_response({"message":"Could not perform checkout"}, 400))

#    # UPDATING TOTAL INVENTORY AND CHECKED OUT COUNT
#     video.total_inventory -= 1 
#     customer.videos_checked_out_count += 1

#     new_rental = Rental(video_id = video.id,
#                         customer_id = customer.id,
#                         due_date = datetime.date.today() + datetime.timedelta(days=7),
#                         status = "checked out" 
#                         )

#     check_out_response = {"customer_id": new_rental.customer_id,
#                             "video_id": new_rental.video_id,
#                             "due_date": new_rental.due_date,
#                             "videos_checked_out_count": rental_count + 1,
#                             "available_inventory": available_inventory - 1
#                             } 
#     db.session.add(new_rental)
#     db.session.commit()

#     return make_response(jsonify(check_out_response), 200)