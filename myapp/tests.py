from django.test import TestCase

# Create your tests here.
$(document).ready(function() {
    // ... (các phần mã trước đó)

    // xử lý click vào nút tạo đơn hàng
    $('button[type="button"]').on('click', function() {
        const sanPhams = []; // Khai báo bên ngoài vòng lặp
        const soLuongs = []; // Khai báo bên ngoài vòng lặp

        // Lấy dữ liệu từ bảng danh sách sản phẩm
        $('#danh_sach_san_pham tbody tr').each(function() {
            const sanPham = $(this).find('td:first-child').text();
            const soLuong = $(this).find('input[name="so_luong[]"]').val();
            sanPhams.push(sanPham);
            soLuongs.push(soLuong);
        });

        // Chuẩn bị dữ liệu để gửi
        const data = {
            so_dien_thoai: $('#so_dien_thoai').val(), // Lấy giá trị
            ten_khach_hang: $('#ten_khach_hang').val(), // Lấy giá trị
            'san_pham[]': sanPhams,
            'so_luong[]': soLuongs,
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
        };

        console.log("Dữ liệu gửi đi:", data); // In ra dữ liệu để kiểm tra

        // Kiểm tra dữ liệu trước khi gửi
        if (sanPhams.length > 0 && soLuongs.length > 0) {
            // Gửi dữ liệu đến backend Django bằng AJAX
            $.ajax({
                url: '/don-hang/tao/', // Đảm bảo URL chính xác
                method: 'POST',
                data: data,
                success: function(response) {
                    // Xử lý phản hồi từ backend
                    console.log(response);
                    // Có thể chuyển hướng người dùng hoặc hiển thị thông báo thành công
                    window.location.href = '/xem-don-hang/'; // Chuyển hướng đến trang xem đơn hàng
                },
                error: function(error) {
                    // Xử lý lỗi
                    console.error(error);
                    // Hiển thị thông báo lỗi cho người dùng
                }
            });
        } else {
            alert("Vui lòng thêm sản phẩm vào đơn hàng.");
        }
    });

    // ... (các phần mã sau đó)
});